
import math

class servo():
    
    MIN_PULSE_MS = 1.0     
    MAX_PULSE_MS = 2.0     
    PERIOD_MS    = 20.0 
    
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
        self.LINK1 = upper_arm_length
        self.LINK2 = forearm_length
    

    def convert_to_servo_angles(self, x_voltage, y_voltage):
        """
        Convert X and Y voltages to servo angles for shoulder and elbow.
        Input: float x_voltage, float y_voltage
        Output: tuple (shoulder_angle, elbow_angle)
        Description: Uses trigonometric transformations to calculate servo angles.
        """
        r2 = x_voltage*x_voltage + y_voltage*y_voltage 
        c = (r2 - self.LINK_1*self.LINK_1 - self.LINK_2*self.LINK_2) / (2 * self.LINK_1 * self.LINK_2) 

        # unreachable positions
        if c < -1 or c > 1:
            raise ValueError("point outside reach")

        beta = math.acos(c)
        alpha = math.atan2(x_voltage, y_voltage) - math.atan2(self.LINK_2 * math.sin(beta), self.LINK_1 + self.LINK_2 * math.cos(beta))

        return (math.degrees(alpha), math.degrees(beta))


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
            if angle_deg < 0: angle_deg = 0
            if angle_deg > 180: angle_deg = 180
            pulse_ms = self.MIN_PULSE_MS + (angle_deg / 180) * (self.MAX_PULSE_MS - self.MIN_PULSE_MS)
            duty_fraction = pulse_ms / self.PERIOD_MS
            duty_u16 = int(duty_fraction * 65535)   
            signals.append(duty_u16)
            
        self.servo_shoulder(signals[0])
        self.servo_elbow(signals[1])
            
            
