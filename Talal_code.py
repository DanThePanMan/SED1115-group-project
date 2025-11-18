from machine import ADC , PWM , I2C, Pin
import math, time
from ads1x15 import ADS1015 

i2c = I2C(1, sda=Pin(14), scl=Pin(15))


pot_x = ADC(Pin(26))     
pot_y = ADC(Pin(27))      


# # 2 define SERVOS 

# servo_shoulder = PWM(Pin(0))   # GP0
# servo_elbow    = PWM(Pin(1))   # GP1

# servo_shoulder.freq(50)   # hobby servos = 50 Hz
# servo_elbow.freq(50)


# Define physical dimmesions in milimeters 

# LINK_1 = 155    # upper arm length
# LINK_2 = 155    # forearm length
# MARGIN = 15     # keep away from extreme edges

have_ads = False
try:
    adc = ADS1015(i2c, 0x48, 1)         # address 0x48 on your board
    have_ads = True
    print("ADS1015 found on I2C.")
except Exception as e:
    print("ADS1015 not found or init failed:", e)

def read_rc_voltage():
    """
    Read RC-filtered PWM voltage on AIN2 (channel 2).
    Returns voltage in volts (float), or None if ADS not available.
    """
    if not have_ads:
        return None
    mv = adc.read(0, 2)     # config=0, channel=2 (AIN2)
    return mv / 1000.0      # convert mV → V

    
# def map_range(value, input_low, input_high, output_low, output_high):
#     ''' we take our value from the pot thats been converted and set a maximum and minimum
#         output and iput value a bounds we cant escape'''
#     return output_low + (output_high - output_low) * ((value - input_low) / (input_high - input_low))



# def ik_two_link(x, y): # function for inverse kinematic eqautions 
#     r2 = x*x + y*y 
#     c = (r2 - LINK_1*LINK_1 - LINK_2*LINK_2) / (2 * LINK_1 * LINK_2) 

#     # unreachable positions
#     if c < -1 or c > 1:
#         raise ValueError("point outside reach")

#     beta = math.acos(c)
#     alpha = math.atan2(y, x) - math.atan2(LINK_2 * math.sin(beta), LINK_1 + LINK_2 * math.cos(beta))

#     return math.degrees(alpha), math.degrees(beta) # return degrees of shoulder and elbow 

# def angle_to_pwm(angle_deg): # function to make the angle back to a pwm singnal 
#     if angle_deg < 0: angle_deg = 0
#     if angle_deg > 180: angle_deg = 180

#     MIN_PULSE_MS = 1.0     # 1.0 ms → 0 deg
#     MAX_PULSE_MS = 2.0     # 2.0 ms → 180 deg
#     PERIOD_MS    = 20.0    # 50 Hz → 20 ms

#     pulse_ms = MIN_PULSE_MS + (angle_deg / 180) * (MAX_PULSE_MS - MIN_PULSE_MS)
#     duty_fraction = pulse_ms / PERIOD_MS
#     duty_u16 = int(duty_fraction * 65535)

#     return duty_u16

# the main
while True:
    # Read pots (0–65535)
    # raw_x = pot_x.read_u16()
    # raw_y = pot_y.read_u16()

    # #  Map pots → workspace mm
    # x_mm = map_range(raw_x, 0, 65535, 30 , 240)
    # y_mm = map_range(raw_y, 0, 65535, 40 ,200)

    # try:
    #     # IK  to int angles
    #     shoulder_deg, elbow_deg = ik_two_link(x_mm, y_mm)

    #     # 4–5) Angles to PWM
    #     pwm_shoulder = angle_to_pwm(shoulder_deg)
    #     pwm_elbow    = angle_to_pwm(elbow_deg)

    #     # Drive servos
    #     servo_shoulder.duty_u16(pwm_shoulder)
    #     servo_elbow.duty_u16(pwm_elbow)

    # except ValueError:
    #     print("Unreachable target:", x_mm, y_mm)

    # RC filter: measure filtered PWM voltage on AIN2
    rc_volt = read_rc_voltage()
    