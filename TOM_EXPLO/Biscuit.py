# Classe Biscuit


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