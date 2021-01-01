#!/usr/bin/python3

import bluetooth
import RPi.GPIO as GPIO

import threading
import time
import logging
logger = logging.getLogger(__name__)

#
# Light Controller
#
class LightController():
    def __init__(self, name, led_id):
        self.name = name
        self.led_id = led_id
        self.state = 0
        self.laststate = 0
        self.led_timer = 0
        
        GPIO.setup(self.led_id, GPIO.OUT)
        GPIO.output(self.led_id, 0)
        
        self._running = True
        self.thread = threading.Thread(target=self.run, name=name)
        self.thread.start()
    
    def setState(self, led_state, led_timer):
        self.state = led_state
        self.led_timer = led_timer

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            time.sleep(0.05)
            if self.laststate != self.state and self.led_timer == 0:
                logger.info ("LED {0} GPIO {1} STATE {2}".format(self.led_id, self.name, self.state))
                GPIO.output(self.led_id, self.state)
                self.laststate = self.state
            
            if self.led_timer > 0:
                time.sleep(self.led_timer)
                logger.info ("LED {0} GPIO {1} STATE {2}".format(self.led_id, self.name, self.state))
                GPIO.output(self.led_id, self.state)
                if (self.state == '1'): self.state = '0'
                elif (self.state == '0'): self.state = '1'


#
# Main method
# 
if __name__ == "__main__":
    #
    # Start the logger
    #
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Starting LED control")
    
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

    #
    # Start the lights
    #
    controller_left = LightController('Left', LEFT_LED)
    controller_right = LightController('Right', RIGHT_LED)
    controller_1 = LightController('One', LIGHT1_LED)

    #
    # Define the server socket
    #
    logger.info("Starting bluetooth controller")
    server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = 1
    server_socket.bind(("", port))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    logger.info("Accepted connection from " + str(address))

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        logger.info ("Received: %s" % data)

        if (data == "0,1,0;"):    
            controller_left.setState(1, 0)

        elif (data == "0,0,0;"):    
            controller_left.setState(0, 0)
        
        elif (data == "1,1,0;"):    
            controller_right.setState(1, 0)

        elif (data == "1,0,0;"):    
            controller_right.setState(0, 0)

        elif (data == "2,1,0;"):    
            controller_1.setState(1, 0)

        elif (data == "2,0,0;"):
            controller_1.setState(0, 0)

        elif (data == "q"):
            logger.info ("Quit")
            controller_left.terminate()
            controller_right.terminate()
            controller_1.terminate()
            break
    
    client_socket.close()
    server_socket.close()
