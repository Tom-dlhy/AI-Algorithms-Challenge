from Biscuit import *

class Dough:
    def __init__(self, length):
        """
        Initialize a Dough object with a specific length.

        Parameters:
        - length (int): Length of the dough.
        """
        self.LENGTH = length
        self.defects_list = []  # tuples (position, class)
        self.biscuits_placed = []  # tuples (position, biscuit_type, valid)

    def add_defect(self, position, defect_class):
        """
        Add a defect to the dough at a specific position.

        Parameters:
        - position (int): Position of the defect on the dough.
        - defect_class (str): Class of the defect ('a', 'b', 'c').
        """
        if 0 <= position < self.LENGTH:
            self.defects_list.append((position, defect_class))
        else:
            raise ValueError("Defect position out of dough range")

    def count_defects(self, position, length):
        """
        Count the number of defects in a specific section of the dough.

        Parameters:
        - position (int): Starting position of the section.
        - length (int): Length of the section to check for defects.

        Returns:
        - dict: Dictionary containing counts of each defect class in the specified section.
        """
        defect_counts = {}
        for pos, cls in self.defects_list:
            if position <= pos < position + length:
                defect_counts[cls] = defect_counts.get(cls, 0) + 1
        return defect_counts

    def place_biscuits(self, biscuits):
        """
        Place biscuits on the dough, ensuring they fit and meet defect requirements.

        Parameters:
        - biscuits (list): List of Biscuit objects to place on the dough.
        """
        self.biscuits_placed.clear()
        current_position = 0
        for biscuit in biscuits:
            if current_position + biscuit.length > self.LENGTH:
                break  # Stop if there's not enough space left for the current biscuit
    
            defect_counts = self.count_defects(current_position, biscuit.length)
            valid = all(defect_counts.get(cls, 0) <= biscuit.max_defects[cls] for cls in biscuit.max_defects)
            self.biscuits_placed.append((current_position, biscuit.biscuit_type, valid))
            current_position += biscuit.length
            self.biscuits_placed = sorted(self.biscuits_placed, key=lambda x: x[0])

    def place_biscuits_GA(self, biscuit_positions):
        """
        Place biscuits on the dough using a Genetic Algorithm approach.

        Parameters:
        - biscuit_positions (list): List of tuples containing (position, biscuit_type).
        """
        self.biscuits_placed.clear()
        for position, biscuit_type in biscuit_positions:
            biscuit = Biscuit(biscuit_type)
            if position + biscuit.length > self.LENGTH:
                break  
            defect_counts = self.count_defects(position, biscuit.length)
            valid = all(defect_counts.get(cls, 0) <= biscuit.max_defects[cls] for cls in biscuit.max_defects)
            self.biscuits_placed.append((position, biscuit.biscuit_type, valid))
            self.biscuits_placed = sorted(self.biscuits_placed, key=lambda x: x[0])

    def get_positions(self):
        """
        Print the positions of all biscuits placed on the dough.
        """
        for position, biscuit_type, is_valid in self.biscuits_placed:
            print(f"biscuit type: {biscuit_type}, position: {position}")
    
    def calculate_total_value(self, solution):
        """
        Calculate the total value of a given solution of placed biscuits.

        Parameters:
        - solution (list): List of tuples containing (position, biscuit_type, is_valid).

        Returns:
        - int: Total value of valid biscuits in the solution.
        """
        total_value = 0
        for position, biscuit_type, is_valid in solution:
            defect = self.count_defects(position, Biscuit(biscuit_type).length)
            print(f"position: {position}, biscuit_type: {biscuit_type}, defect: {defect}, isValid: {is_valid}")
            if is_valid:
                total_value += Biscuit(biscuit_type).value
        return total_value

    def calculate_own_value(self, biscuits):
        """
        Calculate the total value of the biscuits currently placed on the dough, including penalties for unused positions.

        Parameters:
        - biscuits (dict): Dictionary of Biscuit objects indexed by their type.

        Returns:
        - int: Total value of valid biscuits currently placed on the dough, minus penalty for unused positions.
        """
        total_value = 0
        occupied_positions = set()

        for position, biscuit_type, is_valid in self.biscuits_placed:
            if is_valid:
                biscuit = biscuits[biscuit_type]
                biscuit_range = range(position, position + biscuit.length)

                # Check if biscuit fits within the dough length
                if position + biscuit.length > self.LENGTH:
                    is_valid = False  # Biscuit exceeds dough length
                else:
                    # Update occupied positions
                    occupied_positions.update(biscuit_range)
                    total_value += biscuit.value

        # Calculate penalty for unused positions
        total_positions = set(range(self.LENGTH))
        unused_positions = total_positions - occupied_positions
        penalty = -len(unused_positions)
        total_value += penalty  # Subtract penalty from total value

        return total_value


    def validate_biscuits_placement(self, biscuits):
        """
        Validate that all biscuits are correctly placed on the dough without overlapping.

        Parameters:
        - biscuits (list): List of Biscuit objects.

        Returns:
        - tuple: (bool, str) indicating whether the placement is valid and a message.
        """
        last_position = -1
        for position, biscuit_type, is_valid in self.biscuits_placed:
            biscuit = biscuits[biscuit_type]

            # Checks for overlapping
            if position < last_position:
                return False, f"Overlapping detected at position {position} for biscuit type {biscuit_type}."
            last_position = position + biscuit.length

        return True, "All biscuits are correctly placed and within defect thresholds."

    def is_overlapping(self, new_position, new_length, existing_biscuits):
        """
        Check if a new biscuit placement overlaps with existing biscuits.

        Parameters:
        - new_position (int): Position of the new biscuit.
        - new_length (int): Length of the new biscuit.
        - existing_biscuits (list): List of tuples containing (position, biscuit_type).

        Returns:
        - bool: True if the new placement overlaps, False otherwise.
        """
        for position, biscuit_type in existing_biscuits:
            biscuit_length = Biscuit(biscuit_type).length
            if not (new_position + new_length <= position or new_position >= position + biscuit_length):
                return True 
        return False 

    def __str__(self):
        """
        Return a string representation of the dough, including defects and biscuits placed.

        Returns:
        - str: String representation of the dough's defects and biscuits placed.
        """
        result = "Dough Defects:\n"
        for pos, cls in self.defects_list:
            result += f"Position: {pos:.2f}, Class: {cls}\n"
        result += "\nBiscuits Placed:\n"
        for pos, b_type, valid in self.biscuits_placed:
            result += f"Position: {pos}, Biscuit Type: {b_type}, Valid: {valid}\n"
        return result
    

    def defects(self):
        """
        Get the list of defects on the dough.

        Returns:
        - list: List of tuples containing (position, class) of defects.
        """
        return self.defects_list

    def biscuits(self):
        """
        Get the list of biscuits placed on the dough.

        Returns:
        - list: List of tuples containing (position, biscuit_type, valid).
        """
        return self.biscuits_placed
