#!/usr/bin/python3

import bluetooth
import RPi.GPIO as GPIO

#
# Define the raspberrypi leds
#
LEFT_LED=21
RIGHT_LED=20
LIGHT1_LED=16

#
# Programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
#
GPIO.setmode(GPIO.BCM)     
GPIO.setwarnings(False)
GPIO.setup(LEFT_LED, GPIO.OUT)
GPIO.setup(RIGHT_LED, GPIO.OUT)
GPIO.setup(LIGHT1_LED, GPIO.OUT)  

#
# Start the lights
#
GPIO.output(LEFT_LED, 0)
GPIO.output(RIGHT_LED, 0)
GPIO.output(LIGHT1_LED, 0)

#
# Define the server socket
#
server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
 
port = 1
server_socket.bind(("", port))
server_socket.listen(1)
client_socket, address = server_socket.accept()
print ("Accepted connection from " + str(address))

#
# Main thread
#
while 1:
    data = client_socket.recv(1024).decode('utf-8')
    print ("Received: %s" % data)

    if (data == "0,1,0;"):    
        #if '1' is sent from the Android App, turn OFF the LED
        print ("GPIO 21 HIGH (LEFT LED) ON")
        GPIO.output(LEFT_LED, 1)

    elif (data == "0,0,0;"):    
        #if '0' is sent from the Android App, turn OFF the LED
        print ("GPIO 21 LOW (LEFT LED) OFF")
        GPIO.output(LEFT_LED, 0)
    
    elif (data == "1,1,0;"):    
        print ("GPIO 20 HIGH (RIGHT_LED) ON")
        GPIO.output(RIGHT_LED, 1)

    elif (data == "1,0,0;"):    
        print ("GPIO 20 LOW (RIGHT_LED) OFF")
        GPIO.output(RIGHT_LED, 0)

    elif (data == "2,1,0;"):    
        print ("GPIO 16 HIGH (LIGHT1_LED) ON")
        GPIO.output(LIGHT1_LED, 1)

    elif (data == "2,0,0;"):
        print ("GPIO 16 LOW (LIGHT1_LED) OFF")
        GPIO.output(LIGHT1_LED, 0)

    elif (data == "q"):
        print ("Quit")
        break
 
client_socket.close()
server_socket.close()