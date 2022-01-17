import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import threading
import sys
import os

#Un-comment this if using OS-X.
os.system('defaults write org.python.python ApplePersistenceIgnoreState NO')

WindowSize = 5000
SampleRate = 1000.0
VoltsPerBit = 2.5/256

#Define global variables
data = []
displayData = [-2 for i in range(WindowSize)]

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
    #print(np.mean(data))


#Handle command line arguments to get IP address
if (len(sys.argv) == 2):
    try:
        UDP_IP = sys.argv[1]
        socket.inet_aton(UDP_IP)
    except:
        sys.exit('Invalid IP address, Try again')
else:
    sys.exit('EMG_Acquire <Target IP Address>')
#UDP_IP = '192.168.42.13'
socket.inet_aton(UDP_IP)


#Connect the UDP_Port
UDP_PORT = 9000
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#Setup plot parameters
fig, ax = plt.subplots()
line, = ax.plot([], '-r') #red line, no points
plt.xlim([0,WindowSize/SampleRate])
plt.ylim([-VoltsPerBit*128,VoltsPerBit*128]) #samples will vary from 0 to 255
plt.xlabel('Time (Seconds)')
plt.ylabel('EMG (mV)')

#This function updates what data is displayed. It will be called in a separate thread created by the animation.FuncAnimation command
def animate(i):
  global displayData, data

  newData = list(data)
  #print(np.mean(newData))
  data = []
  newDisplay = list(displayData[len(newData):len(displayData)] + newData)
  displayData = list(newDisplay)
  line.set_ydata([i*VoltsPerBit-1.25 for i in displayData])
  return line,

#Init only required for blitting to give a clean slate.
def init():
  line.set_xdata([i/SampleRate for i in range(WindowSize)])
  line.set_ydata([i for i in displayData])
  return line,

print('Connected to ', str(UDP_IP))
print("Listening for incoming messages...")
print('Close Plot Window to exit')

#Start a new thread to listen for data over UDP
thread = threading.Thread(target=data_listener)
thread.daemon = True
thread.start()

#Start a new thread to update the plot with acquired data
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init, interval=25, blit=True)

#Show the plot
plt.show()
