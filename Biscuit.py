class Biscuit:
    def __init__(self, biscuit_type):
        """
        Initialize a Biscuit object with a specific type.

        Parameters:
        - biscuit_type (int): An integer representing the type of biscuit.
        """
        self.biscuit_type = biscuit_type
        self.length, self.value, self.max_defects = self._configure_biscuit(biscuit_type)

    def _configure_biscuit(self, biscuit_type):
        """
        Configure the biscuit's properties based on its type.

        Parameters:
        - biscuit_type (int): The type of biscuit to configure.

        Returns:
        - length (int): Length of the biscuit.
        - value (int): Value of the biscuit.
        - max_defects (dict): Maximum allowable defects by class ('a', 'b', 'c').
        """
        if biscuit_type == 0:
            return 4, 3, {'a': 4, 'b': 2, 'c': 3}
        elif biscuit_type == 1:
            return 8, 12, {'a': 5, 'b': 4, 'c': 4}
        elif biscuit_type == 2:
            return 2, 1, {'a': 1, 'b': 2, 'c': 1}
        elif biscuit_type == 3:
            return 5, 8, {'a': 2, 'b': 3, 'c': 2}
        elif biscuit_type == 4:
            return 1, -1, {'a': 10, 'b': 10, 'c': 10} # This biscuit serves for some heuristics
        else:
            return 1, -1, {'a': 10, 'b': 10, 'c': 10}

    def biscuit_type(self):
        return self.biscuit_type
    
    def value(self):
        return self.value
    
    def length(self):
        return self.length
    
    def max_defects(self):
        """
        Get the maximum allowable defects for the biscuit.

        Returns:
        - dict: Dictionary containing maximum allowable defects for each class ('a', 'b', 'c').
        """
        return self.max_defects
    
    def __str__(self):
        return f"Biscuit Type: {self.biscuit_type}, Length: {self.length}, Value: {self.value}, Max Defects: {self.max_defects}"