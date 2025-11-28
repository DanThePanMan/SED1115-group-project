from machine import ADC , PWM , I2C, Pin
import math, time
from ads1x15 import ADS1015 
from utils import servo, reader

# some config

pot_x = ADC(Pin(26))     
pot_y = ADC(Pin(27)) 

servo_shoulder = PWM(Pin(0))  
servo_elbow    = PWM(Pin(1)) 

LINK_1 = 155    # upper arm length (mm)
LINK_2 = 155    # forearm length (mm)


# object init
Servo = servo.Servo(servo_shoulder, servo_elbow, 50, LINK_1, LINK_2)
reader = reader.Potentiometer(pot_x, pot_y)

print("IK robot ready – moving with pots")

while True:
    # read potentiometer
    x_mm = reader.read_potentiometer_x()
    y_mm = reader.read_potentiometer_y()

    try:
        # IK to servo angles (now returns calibrated servo angles)
        shoulder_deg, elbow_deg = Servo.convert_to_servo_angles(x_mm, y_mm)

        # convert angles and drive arm
        Servo.set_servo_angles(shoulder_deg, elbow_deg)

    except ValueError:
        # Point is unreachable – just ignore this position
        pass

    time.sleep(0.02)
    
    # RC filter: measure filtered PWM voltage on AIN2
    # rc_volt = read_rc_voltage()
