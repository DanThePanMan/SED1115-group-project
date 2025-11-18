from machine import ADC , PWM , I2C, Pin
import math, time
from ads1x15 import ADS1015 
from utils import servo, reader

# some config

pot_x = ADC(Pin(26))     
pot_y = ADC(Pin(27)) 

servo_shoulder = PWM(Pin(0))  
servo_elbow    = PWM(Pin(1)) 

LINK_1 = 155    # upper arm length
LINK_2 = 155    # forearm length

# todo: migrate main logic from the file
# object init
Servo = servo.Servo(servo_shoulder, servo_elbow, 50, LINK_1, LINK_2)
reader = reader.Potentiometer(pot_x, pot_y)


# read potentiometer
raw_x = reader.read_potentiometer_x()
raw_y = reader.read_potentiometer_y()

# map potentimeter
x_mm = reader.map_range(raw_x, 0, 65535, 30 , 240)
y_mm = reader.map_range(raw_y, 0, 65535, 40 ,200)


try:
    # IK to int angles
    shoulder_deg, elbow_deg = Servo.convert_to_servo_angles(x_mm, y_mm)

    # convert angles and drive arm
    pwm_shoulder = Servo.set_servo_angles(shoulder_deg)
    pwm_elbow    = Servo.set_servo_angles(elbow_deg)

except ValueError:
    print("Unreachable target:", x_mm, y_mm)

    # RC filter: measure filtered PWM voltage on AIN2

    # rc_volt = read_rc_voltage()
