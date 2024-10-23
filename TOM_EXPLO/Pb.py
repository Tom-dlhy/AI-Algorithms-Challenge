
import math

class Biscuit:
    def __init__(self, name, length, value, defects_thresholds):
        """
        Initialise un biscuit avec un nom, une taille (length), une valeur (value), et des seuils de défauts (defects_thresholds).
        """
        self.name = name
        self.length = length
        self.value = value
        self.defects_thresholds = defects_thresholds  # {'a': max_defects_a, 'b': max_defects_b, 'c': max_defects_c}

    def can_place(self, start_pos, defects):
        """
        Vérifie si le biscuit peut être placé à partir de la position start_pos en respectant les contraintes de défauts.
        """
        # Sélectionner les défauts dans la plage couverte par le biscuit
        covered_defects = defects[(defects['x'] >= start_pos) & (defects['x'] < start_pos + self.length)]

        # Compter les défauts par classe dans cette plage
        defect_counts = covered_defects['class'].value_counts().to_dict()

        # Vérifier si chaque classe de défauts respecte les seuils
        for defect_class, max_allowed in self.defects_thresholds.items():
            if defect_counts.get(defect_class, 0) > max_allowed:
                return False
        return True

    def __repr__(self):
        return f"Biscuit(name={self.name}, length={self.length}, value={self.value}, defects_thresholds={self.defects_thresholds})"



class Chunk:
    def __init__(self, position, defects, is_occupied):
        """
        Initialize a chunk with a position and a dictionary of defects.
        
        Args:
            position (float): The starting position of the chunk.
            defects (dict): A dictionary of defects, where the keys are defect types (e.g., 'a', 'b', 'c')
                            and the values are the counts of each defect in the chunk.
        """
        self.position = position
        self.defects = defects
        self.is_occupied = is_occupied

    def __repr__(self):
        """
        String representation of the chunk object.
        """
        return f"Chunk(position={self.position}, defects={self.defects}, is occupied={self.is_occupied})"


class BiscuitOptimization:
    def __init__(self, defects, num_chunks=500, _biscuits=None):
        """
        Initialize the BiscuitOptimization with defects, biscuits, and chunks.

        Args:
            defects (list or DataFrame): A list or dataframe containing defect data.
            num_chunks (int): The number of chunks the problem is divided into (default 500).
            biscuits (list): A list of Biscuit objects (default None, will initialize default biscuits).
        """
        self.num_chunks = num_chunks  # Total number of chunks (default to 500)
        self.defects = defects  # Assign the defects data
        self.current_chunk_pos = 0
        
        # Initialize biscuits if not provided
        if _biscuits is None:
            self._biscuits = [
                Biscuit(name="Biscuit_0", length=4, value=3, defects_thresholds={'a': 4, 'b': 2, 'c': 3}),
                Biscuit(name="Biscuit_1", length=8, value=12, defects_thresholds={'a': 5, 'b': 4, 'c': 4}),
                Biscuit(name="Biscuit_2", length=2, value=1, defects_thresholds={'a': 1, 'b': 2, 'c': 1}),
                Biscuit(name="Biscuit_3", length=5, value=8, defects_thresholds={'a': 2, 'b': 3, 'c': 2}),
                Biscuit(name="no_biscuit", length=1, value=-1, defects_thresholds={'a': float('inf'), 'b': float('inf'), 'c': float('inf')})
            ]
        else:
            self._biscuits = _biscuits

        # Initialize chunks
        self._chunks = []
        for i in range(num_chunks):
            # Extract defects at the exact chunk position
            chunk_defects = defects[defects['x'].apply(math.floor) == i]

            # Count the defects by type (e.g., 'a', 'b', 'c')
            defects_count = chunk_defects['class'].value_counts().to_dict()

            # Add chunk with its position, defects, and is_occupied = False
            self._chunks.append(Chunk(position=i, defects=defects_count, is_occupied=False))
    
    def can_place_biscuit(self, start_pos, biscuit):
        if(biscuit.length + start_pos < self.num_chunks) == False:
            return False
        else:
            return True

    def actions(self):
        possible_actions = []
        current_pos = self.current_chunk_pos
        max = self.num_chunks
        for biscuit in self._biscuits:
            if(self.can_place_biscuit(current_pos, biscuit, max)):
                possible_actions.append(biscuit)
        return possible_actions
    
    def result(self, state, action):
        if(action.name == 'Biscuit_0'):
            return True

