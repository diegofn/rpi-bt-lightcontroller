#!/usr/bin/python3

import bluetooth
import RPi.GPIO as GPIO

import threading
import time
import logging
import re

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

        logger.info("Starting LED thread")
        GPIO.setup(self.led_id, GPIO.OUT)
        GPIO.output(self.led_id, 0)
        
        self._running = True
        self.thread = threading.Thread(target=self.run, name=name)
        self.thread.start()
    
    def setState(self, led_state, led_timer):
        self.state = int(led_state)
        self.led_timer = int(led_timer)

        #
        # Enable/disable the timer
        #
        if int(led_timer) > 0:
            self.laststate = int(led_state)

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            time.sleep(0.05)
            if self.laststate != self.state and self.led_timer == 0:
                logger.info ("LED {0} GPIO {1} STATE {2}".format(self.name.ljust(5), self.led_id, self.state))
                GPIO.output(self.led_id, self.state)
                self.laststate = self.state
            
            if self.led_timer > 0 and self.laststate == 1:
                time.sleep(self.led_timer / 1000)
                logger.info ("LED {0} GPIO {1} STATE {2} TIMER {3}".format(self.name.ljust(5), self.led_id, self.state, self.led_timer))
                GPIO.output(self.led_id, self.state)
                if (self.state == 1): self.state = 0
                elif (self.state == 0): self.state = 1


#
# Main method
# 
if __name__ == "__main__":
    #
    # Start the logger
    #
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Starting LED and Bluethoot control")
    
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
    while True:
        client_socket, address = server_socket.accept()
        logger.info("Accepted connection from " + str(address))

        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                logger.info ("Received: %s" % data)

                m = re.compile("(\d),(\d),(\d+);").search(data)

                if (m):
                    state = m.group(2)
                    timer = m.group(3)
                    if (m.group(1) == '0'):
                        controller_left.setState(state, timer)

                    elif (m.group(1) == '1'):
                        controller_right.setState(state, timer)
                    
                    elif (m.group(1) == '2'):
                        controller_1.setState(state, timer)

                if (data == "q"):
                    logger.info ("Quit")
                    break

            except bluetooth.btcommon.BluetoothError as error:
                logger.info ("Caught BluetoothError: %s" % error)
                time.sleep(0.5)
                client_socket.close()
                break
    
        if (data == "q"):
            controller_left.terminate()
            controller_right.terminate()
            controller_1.terminate()
            break

    client_socket.close()
    server_socket.close()
