from machine import ADC , PWM , I2C, Pin
import math, time
from ads1x15 import ADS1015 
from utils import servo, reader, pen


# some config

pot_x = ADC(Pin(26))     
pot_y = ADC(Pin(27)) 

servo_shoulder = PWM(Pin(0))  
servo_elbow    = PWM(Pin(1)) 

LINK_1 = 155.0    # upper arm length (mm)
LINK_2 = 157.0    # forearm length (mm)

button = Pin(12)

# object init
Servo = servo.Servo(servo_shoulder, servo_elbow, 50, LINK_1, LINK_2)
reader = reader.Potentiometer(pot_x, pot_y)

print("Normalized IK robot ready – pots → [0,1] → IK → servos")


# rc filter code 
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
adc = ADS1015(i2c, 0x48, 1)


def read_rc_filter():
    raw0 = adc.read(rate=4, channel1=0) # shoulder
    raw1 = adc.read(rate=4, channel1=1) # elbow
    return adc.raw_to_v(raw0), adc.raw_to_v(raw1)

def v_to_angle_shoulder(v):
    servo_angle = (v - 1.1) / (1.7 - 1.1) * 180
    geometric_angle = (servo_angle - 160.0) / 1.0
    return geometric_angle

def v_to_angle_elbow(v):
    servo_angle = (v - 1.1) / (1.7 - 1.1) * 180
    geometric_angle = (servo_angle - 172.0) / -1.1
    return geometric_angle


#main loops
while True:
    # read potentiometer (returns normalized [0,1] values)
    x_norm = reader.read_potentiometer_x()
    y_norm = reader.read_potentiometer_y()

    try:
        # IK to servo angles (now uses normalized coords)
        shoulder_deg, elbow_deg = Servo.convert_to_servo_angles(x_norm, y_norm)

        # convert angles and drive arm
        Servo.set_servo_angles(shoulder_deg, elbow_deg)

    except ValueError as e:
        # Point is unreachable – just ignore this position
        pass

    time.sleep(0.02)
    
    # pen logic
    if button.value() == 0:  
        pen.control_pen(True)
    else:  
        pen.control_pen(False)

    # RC filter feedback
    rc_volt = read_rc_filter()
    shoulder_feedback = v_to_angle_shoulder(rc_volt[0])
    elbow_feedback = v_to_angle_elbow(rc_volt[1])
    print("x={:.3f} y={:.3f} | S={:6.1f}° E={:6.1f}° | FB: S={:6.1f}° E={:6.1f}°".format(
        x_norm, y_norm, shoulder_deg, elbow_deg, shoulder_feedback, elbow_feedback
    ))
    

