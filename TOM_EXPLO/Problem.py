# Classe Problem

class Problem:
    def __init__(self, start_position, end_position, defects, biscuits, step):
        """
        Initialize the problem with a start and end position, a list of defects, a list of biscuits, and the step size.
        
        Parameters:
        start_position (float): The starting point of the segment.
        end_position (float): The ending point of the segment.
        defects (DataFrame): The defects data (coordinates and types).
        biscuits (list): A list of available biscuits, including their sizes and values.
        step (float): The size of the smallest unit for placement.
        """
        self.start_position = start_position
        self.end_position = end_position
        self.defects = defects
        self.biscuits = biscuits
        self.step = step

    def is_within_bounds(self, position, biscuit_length):
        """
        Check if the biscuit can be placed within the segment bounds.
        
        Parameters:
        position (float): The current position in the segment.
        biscuit_length (float): The length of the biscuit being placed.
        
        Returns:
        bool: True if the biscuit can be placed within bounds, False otherwise.
        """
        return position + biscuit_length <= self.end_position

    def get_available_biscuits(self):
        """
        Return the list of biscuits that can be placed in the segment.
        
        Returns:
        list: Available biscuits with their sizes and values.
        """
        return self.biscuits

    def count_defects_in_range(self, start, length):
        """
        Count defects in a given range of the segment.
        
        Parameters:
        start (float): Starting position of the range.
        length (float): Length of the range.
        
        Returns:
        dict: A dictionary counting the number of defects of each type in the range.
        """
        defects_in_range = self.defects[(self.defects['x'] >= start) & (self.defects['x'] < start + length)]
        return defects_in_range['class'].value_counts().to_dict()

