import pyglet
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import threading
import sys
import os
import math

#EXTRA CREDIT Import 
######## by: Myriam Hrosz and Kayla Mckeague
######## objective: Show '1' when flexing '0' when relaxed
try:
	from pyfirmata import Arduino, util
except:
	import pip
	pip.main(['install','pyfirmata'])
	from pyfirmata import Arduino, util
import time
board = Arduino('COM3')
counta = board.get_pin('d:2:o') #import for pin A
countb = board.get_pin('d:3:o') #for pin B
countc = board.get_pin('d:4:o') #for pin C
countd = board.get_pin('d:5:o') #for pin D
counte = board.get_pin('d:6:o') #for pin E
countf = board.get_pin('d:7:o') #for pin F
countg = board.get_pin('d:8:o') #for pin G

WindowSize = 5000
SampleRate = 1000.0
VoltsPerBit = 2.5/256

#Define global variables
Fs = 1000
FlexWindowSize = 0.25
data = []
displayData = [-2 for i in range(WindowSize)]
flexing = False

# This reads from a socket.
def data_listener():
  global data
  UDP_PORT = 9000
  sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))
  while True:
    newdata, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data.extend(list(newdata))

#Handle command line arguments to get IP address
if (len(sys.argv) == 2):
    try:
        UDP_IP = sys.argv[1]
        socket.inet_aton(UDP_IP)
    except:
        sys.exit('Invalid IP address, Try again')
else:
    sys.exit('EMG_Acquire <Target IP Address>')

#Connect the UDP_Port
UDP_PORT = 9000
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

print('Connected to ', str(UDP_IP))
print("Listening for incoming messages...")
print('Close Window to exit')

#Start a new thread to listen for data over UDP
thread = threading.Thread(target=data_listener)
thread.daemon = True
thread.start()

#Load and place image resources
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()
ForeArm_image = pyglet.resource.image("forearm.png")
Bicep_image = pyglet.resource.image("Bicep.png")
ForeArm_image.anchor_x = 7
ForeArm_image.anchor_y = ForeArm_image.height-150
Bicep_image.anchor_x = Bicep_image.width/2
Bicep_image.anchor_y = Bicep_image.height/2

#Define the moving ForeArm class
class ForeArm(pyglet.sprite.Sprite):
  def __init__(self, *args, **kwargs):
    super(ForeArm,self).__init__(img=ForeArm_image,*args, **kwargs)	
    self.rotate_speed = 100.0
    self.rotation_upper_limit = -10
    self.rotation_lower_limit = -100
    self.rotation = self.rotation_upper_limit
    self.key_handler = pyglet.window.key.KeyStateHandler()

  def update(self, dt):
    if flexing:
      if not ((self.rotation-self.rotate_speed*dt) <=  self.rotation_lower_limit):
        self.rotation -= self.rotate_speed*dt
      else:
        self.rotation = self.rotation_lower_limit
    else:
      if not((self.rotation+self.rotate_speed*dt) >= self.rotation_upper_limit):
        self.rotation += self.rotate_speed*dt
      else:
        self.rotation = self.rotation_upper_limit


#Setup the main window
main_window = pyglet.window.Window(1000,600)
main_batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
bicep = pyglet.sprite.Sprite(img=Bicep_image,x=350,y=150,batch=main_batch,group=background)
forearm = ForeArm(x=510, y=115,batch=main_batch,group=foreground)
pyglet.gl.glClearColor(1, 1, 1, 1)
main_window.push_handlers(forearm)
main_window.push_handlers(forearm.key_handler)


def update(dt):
  global displayData, data, flexing

  newData = list(data)

  data = []
  newDisplay = list(displayData[len(newData):len(displayData)] + newData)
  displayData = list(newDisplay)

  #Put your flex algorithm code here!
  #If flexing is detected, set the 'flexing' variable to True.
  #Otherwise, set it to False. 
  #############################
  #ALL OF YOUR CODE SHOULD GO BELOW HERE
 
  displayintdata = list(int(x) for x in displayData) #turn display data from bits into integers
  voltagedata = [abs(i*VoltsPerBit-1.25) for i in displayintdata]   #turn integers into volts
  
  print(np.mean(voltagedata[-100::]))   #print mean of voltage data
  
  if np.mean(voltagedata[-100::]) > 0.045:   #determine whether voltage surpasses flexing threshold or not
   flexing = True  #display 1
   counta.write(0) #pin A off
   countb.write(1) #pin B on
   countc.write(1) #pin C on
   countd.write(0) #pin D off
   counte.write(0) #pin E off
   countf.write(0) #pin F off
   countg.write(0) #pin G off
 
  else:
   flexing = False #display 0
   counta.write(1) #pin A on 
   countb.write(1) #pin B on
   countc.write(1) #pin C on
   countd.write(1) #pin D on
   counte.write(1) #pin E on
   countf.write(1) #pin F on
   countg.write(0) #pin G off
 


  #ALL OF YOUR CODE SHOULD GO ABOVE HERE
#__/\\\\\\\\\\\\\____/\\\\____________/\\\\__/\\\\\\\\\\\\\\\_______________/\\\\\\\\\\______/\\\\\\\_________/\\\_        
# _\/\\\/////////\\\_\/\\\\\\________/\\\\\\_\/\\\///////////______________/\\\///////\\\___/\\\/////\\\___/\\\\\\\_       
#  _\/\\\_______\/\\\_\/\\\//\\\____/\\\//\\\_\/\\\________________________\///______/\\\___/\\\____\//\\\_\/////\\\_      
#   _\/\\\\\\\\\\\\\\__\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\_______________________/\\\//___\/\\\_____\/\\\_____\/\\\_     
#    _\/\\\/////////\\\_\/\\\__\///\\\/___\/\\\_\/\\\///////_______________________\////\\\__\/\\\_____\/\\\_____\/\\\_    
#     _\/\\\_______\/\\\_\/\\\____\///_____\/\\\_\/\\\_________________________________\//\\\_\/\\\_____\/\\\_____\/\\\_   
#      _\/\\\_______\/\\\_\/\\\_____________\/\\\_\/\\\________________________/\\\______/\\\__\//\\\____/\\\______\/\\\_  
#       _\/\\\\\\\\\\\\\/__\/\\\_____________\/\\\_\/\\\\\\\\\\\\\\\___________\///\\\\\\\\\/____\///\\\\\\\/_______\/\\\_ 
#        _\/////////////____\///______________\///__\///////////////______________\/////////________\///////_________\///_ 
  ###################################
  forearm.update(dt)


@main_window.event
def on_draw():
    main_window.clear()
    main_batch.draw()

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
