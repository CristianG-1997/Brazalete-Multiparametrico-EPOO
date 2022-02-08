# Joystick controlled mouse
# By Shubham Santosh
# last edited 12/11/2020
import mouse, sys
import time 
import serial

mouse.FAILSAFE=False
ArduinoSerial=serial.Serial(port='COM3', baudrate=115200, timeout=0.1, write_timeout=1)  #Specify the correct COM port
time.sleep(1)                             #delay of 1 second
print('startttt')
data=(ArduinoSerial.readline())    #read the data
time.sleep(5)                             #
while 1:
   try:
           
       data=(ArduinoSerial.readline()).decode('utf-8')    #read the data
       k=str(data)
       Test=k.split()           # assigns to x,y and z
       (X,Y)=mouse.get_position()        #read the cursor's current position
       
       (x,y,z)=(-int(Test[1]),-int(Test[0]),int(Test[2]))
       print(x,y,z)
       #convert to int
       mouse.move(X+x,Y-y)           #move cursor to desired position
       if z==1:                        # read the Status of SW
          mouse.click(button="left")    # clicks left button
   except:
       t=0;
