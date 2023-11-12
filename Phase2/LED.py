#!/usr/bin/env python3
#############################################################################
# Filename    : LED.py
# Description :	Class for LED
# Author      : Rachelle Badua
# modification: 2023/10/23
########################################################################
import RPi.GPIO as GPIO

class LED():
    # Setup LED 
    led_pin = 0
    state = False

    def __init__(self, led_pin, state):
        self.led_pin = led_pin
        self.state = state

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(led_pin, GPIO.OUT, initial=state)
        # GPIO.output(led_pin, GPIO.LOW) 
    
    def switchLight(self, state_LED):
        if state_LED == True:
            GPIO.output(self.led_pin, GPIO.HIGH)
        else: 
            GPIO.output(self.led_pin, GPIO.LOW)

    def turn_on_led(self):
        GPIO.output(self.led_pin, GPIO.HIGH)

    def turn_off_led(self): 
        GPIO.output(self.led_pin, GPIO.LOW)