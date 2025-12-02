class Potentiometer():
    
    def __init__(self, pot_x, pot_y):
        """
        Constructor
        Input: ADC pot_x, ADC pot_y
        Output: None
        Description: object contructor
        """
        self.pot_x = pot_x
        self.pot_y = pot_y
        

    def map_range(self, value, input_low, input_high, output_low, output_high):
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
        Output: float (normalized x coordinate [0,1])
        Description: Reads ADC channel connected to X-axis pot and returns normalized position.
                    x_norm = 0 → right edge, x_norm = 1 → left edge
        """
        raw_x = self.pot_x.read_u16()
        # Normalize to [0,1]
        x_norm = raw_x / 65535.0
        return x_norm

    def read_potentiometer_y(self):
        """
        Read the Y-axis potentiometer value via ADC.
        Input: None
        Output: float (normalized y coordinate [0,1])
        Description: Reads ADC channel connected to Y-axis pot and returns normalized position.
                    y_norm = 0 → top edge, y_norm = 1 → bottom edge
        """
        raw_y = self.pot_y.read_u16()
        # Normalize to [0,1]
        y_norm = raw_y / 65535.0
        return y_norm

