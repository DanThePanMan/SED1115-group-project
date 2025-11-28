

import math

class Servo():
    
    MIN_PULSE_MS = 1.0     
    MAX_PULSE_MS = 2.0     
    PERIOD_MS    = 20.0 
    
    # Geometry / jig constants
    PAPER_WIDTH  = 280        # along X
    PAPER_HEIGHT = 280        # along Y
    PAPER_MIDH   = PAPER_WIDTH / 2.0
    
    # Shoulder base position relative to paper origin (0,0 is bottom-left of paper)
    SHOULDER_X = -50.0
    SHOULDER_Y = PAPER_HEIGHT / 2.0
    
    # Servo calibration: converts geometric angle -> actual servo angle
    SHOULDER_A = 1.0
    SHOULDER_B = 148.0
    ELBOW_A    = -1.1
    ELBOW_B    = 171.11
    
    # Servo safety limits (degrees at the servo horn)
    SHOULDER_MIN = 13.0
    SHOULDER_MAX = 162.0
    ELBOW_MIN    = 40.0
    ELBOW_MAX    = 140.0
    
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
        if v < lo: return lo
        if v > hi: return hi
        return v

    def convert_to_servo_angles(self, x_mm, y_mm):
        """
        Convert X and Y coordinates (in mm) to servo angles for shoulder and elbow.
        Uses improved inverse kinematics with proper coordinate system handling.
        Input: float x_mm, float y_mm (paper coordinates, bottom-left origin)
        Output: tuple (shoulder_angle, elbow_angle) in degrees
        Description: Uses trigonometric transformations to calculate servo angles.
        """
        # Convert paper coords to absolute coords centred on paper mid-height
        cx = x_mm + self.PAPER_MIDH
        cy = y_mm
        
        dx = cx - self.SHOULDER_X
        dy = cy - self.SHOULDER_Y
        
        # Distance AC
        lac = math.sqrt(dx*dx + dy*dy)
        
        # Reach check
        max_reach = self.LINK_1 + self.LINK_2
        if lac <= 0 or lac > max_reach:
            raise ValueError("Outside reachable workspace")
        
        # Eq. (3): cos(theta2)
        cos_t2 = (dx*dx + dy*dy - self.LINK_1*self.LINK_1 - self.LINK_2*self.LINK_2) / (2.0 * self.LINK_1 * self.LINK_2)
        cos_t2 = self.clamp(cos_t2, -1.0, 1.0)
        
        # theta2 via atan2, always positive elbow
        sin_t2 = math.sqrt(max(0.0, 1.0 - cos_t2*cos_t2))
        theta2 = math.atan2(sin_t2, cos_t2)
        
        # Eq. (4) & (5): theta1
        k1 = self.LINK_1 + self.LINK_2 * cos_t2
        k2 = self.LINK_2 * sin_t2
        theta1 = math.atan2(dy, dx) - math.atan2(k2, k1)
        
        # Convert to degrees
        alpha_deg = math.degrees(theta1)
        beta_deg  = math.degrees(theta2)
        
        # Convert to servo angles using calibration
        shoulder_servo = self.SHOULDER_A * alpha_deg + self.SHOULDER_B
        elbow_servo    = self.ELBOW_A * beta_deg  + self.ELBOW_B
        
        # Clamp to safe servo ranges
        shoulder_servo = self.clamp(shoulder_servo, self.SHOULDER_MIN, self.SHOULDER_MAX)
        elbow_servo    = self.clamp(elbow_servo,    self.ELBOW_MIN,    self.ELBOW_MAX)
        
        return (shoulder_servo, elbow_servo)


    def set_servo_angles(self, shoulder_angle, elbow_angle):
        """
        Set PWM signals to move shoulder and elbow servos.
        Input: float shoulder_angle, float elbow_angle
        Output: None
        Description: Generates PWM signals to move servos smoothly.
        """
        angles = [shoulder_angle, elbow_angle]
        signals = []
        for angle_deg in angles:
            # Clamp to 0-180 range
            angle_deg = self.clamp(angle_deg, 0.0, 180.0)
            pulse_ms = self.MIN_PULSE_MS + (angle_deg / 180) * (self.MAX_PULSE_MS - self.MIN_PULSE_MS)
            duty_fraction = pulse_ms / self.PERIOD_MS
            duty_u16 = int(duty_fraction * 65535)   
            signals.append(duty_u16)
            
        self.servo_shoulder.duty_u16(signals[0])
        self.servo_elbow.duty_u16(signals[1])
            
            

            
