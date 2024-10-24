import math
import random
import numpy as np


class Biscuit:
    def __init__(self, name, length, value, defects_thresholds):
        """
        Initialise un biscuit avec un nom, une taille (length), une valeur (value), et des seuils de défauts (defects_thresholds).
        """
        self.name = name
        self.length = length
        self.value = value
        self.defects_thresholds = defects_thresholds  # {'a': max_defects_a, 'b': max_defects_b, 'c': max_defects_c}


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

class State:
    def __init__(self, current_pos = 0, path = None, value = 0):
        self.current_pos = current_pos
        self.path = path if path is not None else []
        self.value = value

    def to_tuple(self):
        """Convertit l'état en un tuple pour l'utiliser dans l'algorithme A*."""
        return (self.current_pos, tuple(self.path), self.value)
        
    def __repr__(self):
        return f"State(pos={self.current_pos}, path={self.path}, value={self.value})"

class BiscuitOptimization:
    def __init__(self, defects, num_chunks=500, _biscuits=None):
        """
        Initialize the BiscuitOptimization with defects, biscuits, and chunks.

        Args:
            defects (list or DataFrame): A list or dataframe containing defect data.
            num_chunks (int): The number of chunks the problem is divided into (default 500).
            biscuits (list): A list of Biscuit objects (default None, will initialize default biscuits).
        """
        self.initial_state=State()
        self.goal=State(500)
        self.num_chunks = max(num_chunks, 500)  # Total number of chunks (default to 500)
        self.defects = defects  # Assign the defects data
        self.current_chunk_pos = 0
        
        # Initialize biscuits if not provided
        if _biscuits is None:
            self._biscuits = [
                Biscuit(name="Biscuit_0", length=int(4*self.num_chunks/500), value=3, defects_thresholds={'a': 4, 'b': 2, 'c': 3}),
                Biscuit(name="Biscuit_1", length=int(8*self.num_chunks/500), value=12, defects_thresholds={'a': 5, 'b': 4, 'c': 4}),
                Biscuit(name="Biscuit_2", length=int(2*self.num_chunks/500), value=1, defects_thresholds={'a': 1, 'b': 2, 'c': 1}),
                Biscuit(name="Biscuit_3", length=int(5*self.num_chunks/500), value=8, defects_thresholds={'a': 2, 'b': 3, 'c': 2}),
                Biscuit(name="no_biscuit", length=1, value=-1*500/self.num_chunks, defects_thresholds={'a': np.inf, 'b': np.inf, 'c': np.inf}),
            ]
        else:
            self._biscuits = _biscuits

        # Initialize chunks
        self._chunks = []
        self.assign_defects_to_chunks()
    
    def assign_defects_to_chunks(self):
        """Assigner les défauts à chaque chunk en fonction de leur position et du nombre total de chunks."""
        chunk_size = 500 / self.num_chunks  # Taille de chaque chunk
        # Initialisation des chunks avec une position et un dictionnaire de défauts vide
        for i in range(self.num_chunks):
            self._chunks.append(Chunk(position=i, defects={'a': 0, 'b': 0, 'c': 0}, is_occupied=False))

        # Itérer sur les défauts pour les assigner aux chunks
        for index, defect in self.defects.iterrows():
            position = defect['x']  # Position continue du défaut
            chunk_index = int(position / chunk_size)  # Calculer dans quel chunk placer le défaut

            # Vérification que chunk_index est dans les bornes
            if 0 <= chunk_index < self.num_chunks:
                defect_type = defect['class']
                # Ajouter le défaut au chunk correspondant
                if defect_type in self._chunks[chunk_index].defects:
                    self._chunks[chunk_index].defects[defect_type] += 1
                else:
                    print(f"Erreur : type de défaut inconnu {defect_type}")
            else:
                print(f"Erreur : chunk_index {chunk_index} hors des bornes pour la position {position}")

        print("Assignation terminée. Vérifiez les chunks pour le contenu des défauts.")
    
    def can_place_biscuit(self, start_pos, biscuit):
        if (start_pos + int(biscuit.length) >= self.num_chunks):  # Conversion en entier ici
            return False
        else:
            a = 0
            b = 0
            c = 0
            for i in range(start_pos, start_pos + int(biscuit.length)):  # Conversion en entier ici
                a += self._chunks[i].defects.get('a', 0)
                b += self._chunks[i].defects.get('b', 0)
                c += self._chunks[i].defects.get('c', 0)

            if a > biscuit.defects_thresholds['a'] or b > biscuit.defects_thresholds['b'] or c > biscuit.defects_thresholds['c']:
                return False

            return True

    def actions(self, state):
        possible_actions = []
        current_pos = state.current_pos
        for biscuit in self._biscuits:
            if(self.can_place_biscuit(current_pos, biscuit)):
                possible_actions.append(biscuit)
        return possible_actions
    
    def result(self, state:State, action):
        new_state=State(current_pos=state.current_pos + action.length, 
                      path=state.path + [(state.current_pos, action.name)], 
                      value=state.value + action.value)
        return new_state
    
    def goal_state(self,state:State):
        """
        Vérifie si tous les chunks sont remplis (c'est-à-dire qu'il n'y a plus de place pour des biscuits).
        
        Args:
            state (State): L'état actuel du problème.
        
        Returns:
            bool: True si tous les chunks sont remplis, sinon False.
        """
        return state.current_pos == self.num_chunks
















### Méthpdes pour génétics

    def initialize_population(self, population_size):
        """
        Crée une population initiale de solutions. Chaque solution est une séquence d'actions (placement de biscuits).

        Args:
            population_size (int): Taille de la population.
        
        Returns:
            list: Liste d'individus (états) représentant la population initiale.
        """
        population = []
        for _ in range(population_size):
            # Générer une séquence d'actions (état) de façon aléatoire
            state = State()  # Créer un état initial
            while not self.is_filled(state):  # Tant que tous les chunks ne sont pas remplis
                possible_actions = self.actions(state)
                if possible_actions:
                    action = random.choice(possible_actions)  # Choisir une action aléatoire
                    self.result(state, action)  # Appliquer l'action à l'état (sans réaffecter)
                else:
                    break
            population.append(state)
        return population

    def fitness(self, state):
        """
        Calcule la valeur de l'état (fitness) en fonction des biscuits placés.

        Args:
            state (State): L'état pour lequel calculer le fitness.
        
        Returns:
            float: Valeur du fitness, ici basée sur la valeur totale des biscuits placés moins les espaces vides.
        """
        total_value = state.value
        # Penalty pour les chunks vides
        empty_chunks = sum(1 for chunk in self._chunks if chunk.is_occupied == False)
        total_value -= empty_chunks  # Pénalise chaque chunk vide
        return total_value

    def selection(self, population, fitness_scores):
        """
        Sélectionne deux individus dans la population en fonction de leur fitness.

        Args:
            population (list): Liste des individus de la population.
            fitness_scores (list): Liste des scores de fitness pour chaque individu.
        
        Returns:
            tuple: Deux individus sélectionnés pour le croisement.
        """
        # Utiliser un mécanisme comme la roulette pour sélectionner en fonction du fitness
        total_fitness = sum(fitness_scores)
        selection_probs = [score / total_fitness for score in fitness_scores]
        
        # Sélectionner deux individus
        parent1 = random.choices(population, weights=selection_probs, k=1)[0]
        parent2 = random.choices(population, weights=selection_probs, k=1)[0]
        
        return parent1, parent2
    
    def crossover(self, parent1, parent2):
        """
        Combine deux parents pour produire un nouvel individu (un état).

        Args:
            parent1 (State): Premier parent.
            parent2 (State): Deuxième parent.
        
        Returns:
            State: Nouvel individu résultant du croisement.
        """
        # Crossover en prenant des éléments des deux parents
        crossover_point = random.randint(0, min(len(parent1.path), len(parent2.path)) - 1)
        child_path = parent1.path[:crossover_point] + parent2.path[crossover_point:]
        
        # Créer un nouvel état à partir du chemin résultant
        child = State(current_pos=child_path[-1][0], path=child_path, value=0)
        for _, biscuit_name in child_path:
            biscuit = next(b for b in self._biscuits if b.name == biscuit_name)
            child.value += biscuit.value
        return child
    
    def mutate(self, individual, mutation_rate=0.1):
        """
        Applique une mutation à un individu avec une probabilité définie.

        Args:
            individual (State): L'individu à muter.
            mutation_rate (float): Probabilité de mutation (par défaut 10%).

        Returns:
            State: L'individu potentiellement muté.
        """
        if random.random() < mutation_rate:
            # Appliquer une mutation : remplacer une action par une autre aléatoire
            mutation_point = random.randint(0, len(individual.path) - 1)
            possible_actions = self.actions(individual)
            if possible_actions:
                new_action = random.choice(possible_actions)
                individual.path[mutation_point] = (individual.path[mutation_point][0], new_action.name)
                individual.value = sum(next(b for b in self._biscuits if b.name == name).value for _, name in individual.path)
        return individual
    
    def evolve_generation(self, population, mutation_rate):
        """
        Fait évoluer la population d'une génération en appliquant sélection, crossover et mutation.
        
        Args:
            population (list): La population actuelle (liste d'individus).
            mutation_rate (float): Le taux de mutation.
        
        Returns:
            list: Nouvelle population après évolution.
        """
        new_population = []
        fitness_scores = [self.fitness(individual) for individual in population]
        
        # Sélection et création de la nouvelle population
        for _ in range(len(population)):
            # Sélection de deux parents
            parent1, parent2 = self.selection(population, fitness_scores)
            
            # Crossover pour créer un enfant
            child = self.crossover(parent1, parent2)
            
            # Mutation potentielle de l'enfant
            child = self.mutate(child, mutation_rate)
            
            # Ajout de l'enfant à la nouvelle population
            new_population.append(child)
        
        return new_population

    def get_best_candidate(self, population):
        """
        Retourne l'individu avec la meilleure valeur dans la population.
        """
        best = max(population, key=lambda individual: self.fitness(individual))
        return best

    def evolve(self, population_size, generations, mutation_rate):
        """
        Evolue la population sur plusieurs générations.

        Args:
            population_size (int): Nombre d'individus dans la population.
            generations (int): Nombre de générations pour l'évolution.
            mutation_rate (float): Taux de mutation à appliquer à chaque génération.
            
        Returns:
            best_solution: Le meilleur individu après l'évolution.
        """
        # Initialisation de la population (tu dois déjà avoir cette logique)
        population = self.initialize_population(population_size)
        
        best_solution = None

        # Boucle sur les générations sans barre de progression
        for generation in range(generations):
            # Évaluation de la population (fitness, sélection, croisement, mutation)
            population = self.evolve_generation(population, mutation_rate)
            
            # Trouver la meilleure solution de la génération courante
            best_candidate = self.get_best_candidate(population)
            
            if best_solution is None or best_candidate.value > best_solution.value:
                best_solution = best_candidate
        
        return best_solution

