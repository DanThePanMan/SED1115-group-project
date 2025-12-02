

import math

class Servo():
    
    MIN_PULSE_MS = 500      # microseconds for 0°
    MAX_PULSE_MS = 2500     # microseconds for 180°
    PERIOD_MS    = 20000    # 50 Hz -> 20 ms period in microseconds
    
    # Geometry / jig constants
    PAPER_WIDTH  = 215.0      # mm along X
    PAPER_HEIGHT = 279.0      # mm along Y
    
    # Shoulder base position relative to paper origin (0,0 is bottom-left of paper)
    SHOULDER_X = -50.0
    SHOULDER_Y = PAPER_HEIGHT / 2.0
    
    # Servo calibration: converts geometric angle -> actual servo angle
    SHOULDER_A = 1.0
    SHOULDER_B = 160.0
    ELBOW_A    = -1.1
    ELBOW_B    = 172.0
    
    # Servo safety limits (degrees at the servo horn)
    SHOULDER_MIN = 5.0
    SHOULDER_MAX = 182.0
    ELBOW_MIN    = 5.0
    ELBOW_MAX    = 180.0
    
    def __init__(self, shoulder_pin, elbow_pin, freq, upper_arm_length, forearm_length):
        """
        Constructor function
        Input: PWM shoulder_pin, PWM elbow_pin, int freq, int upper_arm_length, int forearm_length
        Output: none
        Description: Initialize Servo class with relavent variables 
        """
        self.servo_shoulder = shoulder_pin 
        self.servo_elbow    = elbow_pin   

        self.servo_shoulder.freq(freq)   
        self.servo_elbow.freq(freq)
        self.LINK_1 = upper_arm_length
        self.LINK_2 = forearm_length
    
    def clamp(self, v, lo, hi):
        """Clamp value between lo and hi."""
        return min(hi, max(lo, v))

    def convert_to_servo_angles(self, x_norm, y_norm):
        """
        Convert normalized X and Y coordinates to servo angles for shoulder and elbow.
        Uses improved inverse kinematics with proper coordinate system handling.
        Input: float x_norm, float y_norm (normalized coordinates [0,1])
               x_norm = 0 → right edge,  x_norm = 1 → left edge
               y_norm = 0 → top edge,    y_norm = 1 → bottom edge
        Output: tuple (shoulder_angle, elbow_angle) in servo degrees
        Description: Uses trigonometric transformations to calculate servo angles.
        """
        # Map normalized to paper mm coordinates
        cx = (1.0 - x_norm) * self.PAPER_WIDTH
        cy = (1.0 - y_norm) * self.PAPER_HEIGHT
        
        dx = cx - self.SHOULDER_X
        dy = cy - self.SHOULDER_Y
        
        # Distance AC
        lac = math.sqrt(dx*dx + dy*dy)
        
        # Reach check
        max_reach = self.LINK_1 + self.LINK_2
        if lac == 0 or lac > max_reach:
            raise ValueError("Outside reachable workspace")
        
        # Law of cosines for elbow angle (theta2)
        cos_t2 = (dx*dx + dy*dy - self.LINK_1*self.LINK_1 - self.LINK_2*self.LINK_2) / (2.0 * self.LINK_1 * self.LINK_2)
        cos_t2 = min(1.0, max(-1.0, cos_t2))
        
        # theta2 via atan2, always positive elbow
        sin_t2 = math.sqrt(max(0.0, 1.0 - cos_t2*cos_t2))
        theta2 = math.atan2(sin_t2, cos_t2)
        
        # Shoulder angle (theta1)
        k1 = self.LINK_1 + self.LINK_2 * cos_t2
        k2 = self.LINK_2 * sin_t2
        theta1 = math.atan2(dy, dx) - math.atan2(k2, k1)
        
        # Convert to degrees (joint angles)
        shoulder_deg = math.degrees(theta1)
        elbow_deg    = math.degrees(theta2)
        
        # Map to servo "horn" angles using calibration
        shoulder_servo = self.SHOULDER_A * shoulder_deg + self.SHOULDER_B
        elbow_servo    = self.ELBOW_A * elbow_deg + self.ELBOW_B
        
        # Note: Safety clamping removed to allow full range
        # Servo limits enforced in set_servo_angles if needed
        
        return (shoulder_servo, elbow_servo)


    def set_servo_angles(self, shoulder_angle, elbow_angle):
        """
        Set PWM signals to move shoulder and elbow servos.
        Input: float shoulder_angle, float elbow_angle (servo horn angles in degrees)
        Output: None
        Description: Generates PWM signals to move servos using microsecond timing.
        """
        angles = [shoulder_angle, elbow_angle]
        signals = []
        for angle_deg in angles:
            # Clamp to 0-180 range
            angle_deg = self.clamp(angle_deg, 0.0, 180.0)
            # Calculate pulse width in microseconds
            pulse_us = self.MIN_PULSE_MS + (angle_deg / 180.0) * (self.MAX_PULSE_MS - self.MIN_PULSE_MS)
            # Convert to duty cycle (pulse_us / period_us * 65535)
            duty_u16 = int(pulse_us / self.PERIOD_MS * 65535)
            signals.append(duty_u16)
            
        self.servo_shoulder.duty_u16(signals[0])
        self.servo_elbow.duty_u16(signals[1])
            
            

            
