#!/usr/bin/env python3
#############################################################################
# Filename    : DC_Motor.py
# Description :	Class for DC_Motor
# Author      : Rachelle Badua
# modification: 2023/10/29
########################################################################
import RPi.GPIO as GPIO

class DC_Motor():
    # Setup LED 
    Motor1_pin = 0 # Enable Pin
    Motor2_pin = 0 # Input Pin
    Motor3_pin = 0 # Input Pin
    # motor_pin = 0
    state = False

    def __init__(self, Motor1_pin, Motor2_pin, Motor3_pin, state):
        # self.motor_pin = motor_pin
        self.Motor1_pin = Motor1_pin
        self.Motor2_pin = Motor2_pin
        self.Motor3_pin = Motor3_pin
        self.state = state

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(motor_pin, GPIO.OUT, initial=state)
        GPIO.setup(Motor1_pin,GPIO.OUT, initial=state)
        GPIO.setup(Motor2_pin,GPIO.OUT, initial=state)
        GPIO.setup(Motor3_pin,GPIO.OUT, initial=state)
        # GPIO.output(led_pin, GPIO.LOW) 
    
    def switchMotor(self, state_Motor):
        if state_Motor == True:
            # GPIO.output(self.motor_pin, GPIO.HIGH)
            GPIO.output(self.Motor1_pin,GPIO.HIGH)
            GPIO.output(self.Motor2_pin,GPIO.LOW)
            GPIO.output(self.Motor3_pin,GPIO.HIGH)
        else: 
            GPIO.output(self.Motor1_pin, GPIO.LOW)