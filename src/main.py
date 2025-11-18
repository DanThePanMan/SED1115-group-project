from machine import ADC , PWM , I2C, Pin
import math, time
from ads1x15 import ADS1015 

# some config

pot_x = ADC(Pin(26))     
pot_y = ADC(Pin(27)) 

servo_shoulder = PWM(Pin(0))  
servo_elbow    = PWM(Pin(1)) 

# todo: migrate main logic from the file