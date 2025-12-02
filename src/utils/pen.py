from machine import PWM, Pin
import time

# Servo pulse width constants (in microseconds)
MIN_PULSE_MS = 500      # 0 degrees
MAX_PULSE_MS = 2500     # 180 degrees
PERIOD_MS    = 20000    # 50 Hz -> 20ms period in microseconds

# Pen angles
PEN_UP_ANGLE   = 0   
PEN_DOWN_ANGLE = 45   # placeholder values for now- test to see how far it needs to go

# Initialize pen servo on pin 22
pen_servo = PWM(Pin(2))
pen_servo.freq(50)  # Set frequency to 50 Hz for servo

def angle_to_duty(angle_deg):
    """
    Convert servo angle (0-180 degrees) to 16-bit duty cycle.
    Input: angle_deg (0-180)
    Output: duty_u16 (0-65535)
    """
    # Clamp angle to 0-180
    if angle_deg < 0: 
        angle_deg = 0
    if angle_deg > 180: 
        angle_deg = 180
    
    # Calculate pulse width in microseconds
    pulse_us = MIN_PULSE_MS + (angle_deg / 180.0) * (MAX_PULSE_MS - MIN_PULSE_MS)
    
    # Calculate 16-bit duty cycle
    duty_u16 = int(pulse_us / PERIOD_MS * 65535)
    
    return duty_u16

def control_pen(pen_state):
    """
    Raise or lower the pen based on input state.
    Input: boolean pen_state (True = down, False = up)
    Output: None
    Description: Controls pen servo up or down.
    """
    if pen_state:
        target_angle = PEN_DOWN_ANGLE
        print(f"Pen DOWN ({target_angle}°)")
    else:
        target_angle = PEN_UP_ANGLE
        print(f"Pen UP ({target_angle}°)")

    duty = angle_to_duty(target_angle)
    pen_servo.duty_u16(duty)
    print(f"  Duty: {duty}")


