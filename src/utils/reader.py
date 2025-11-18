class potentiometer():
    
    def __init__(self, pot_x, pot_y):
        """
        Constructor
        Input: ADC pot_x, ADC pot_y
        Output: None
        Description: object contructor
        """
        self.pot_x = pot_x
        self.pot_y = pot_y
        

    def map_range(value, input_low, input_high, output_low, output_high):
        """
        Map a value from one range to another.
        Input: value, input_low, input_high, output_low, output_high
        Output: float (mapped value)
        Description: Takes a value from input range and maps it to output range.
        """
        return output_low + (output_high - output_low) * ((value - input_low) / (input_high - input_low))

    def read_potentiometer_x(self):
        """
        Read the X-axis potentiometer value via ADC.
        Input: None
        Output: float (voltage between 0-3.3V)
        Description: Reads ADC channel connected to X-axis pot and returns voltage.
        """
        raw_x = self.pot_x.read_u16()
        x_mm = self.map_range(raw_x, 0, 65535, 30 , 240)


        return x_mm

    def read_potentiometer_y(self):
        """
        Read the Y-axis potentiometer value via ADC.
        Input: None
        Output: float (voltage between 0-3.3V)
        Description: Reads ADC channel connected to Y-axis pot and returns voltage.
        """
        raw_y = self.pot_y.read_u16()
        y_mm = self.map_range(raw_y, 0, 65535, 40 ,200)
        
        return y_mm

