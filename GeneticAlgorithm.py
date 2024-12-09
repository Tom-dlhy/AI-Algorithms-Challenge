import random
from Biscuit import Biscuit

class GeneticAlgorithm:
    '''
    Class representing a Genetic Algorithm for placing biscuits on a dough.
    '''
    def __init__(self, dough, biscuits, population_size, mutation_rate, crossover_rate):
        '''
        Initialize the Genetic Algorithm.

        Parameters:
        - dough (Dough): The dough object to place biscuits on.
        - biscuits (dict): Dictionary of Biscuit objects indexed by their type.
        - population_size (int): Size of the population.
        - mutation_rate (float): Rate of mutation.
        - crossover_rate (float): Rate of crossover.
        '''
        self.dough = dough
        self.biscuits = biscuits
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.initialize_population()

    def initialize_population(self):
        '''
        Initialize the population with random solutions without overlapping.
        '''
        for _ in range(self.population_size):
            individual = self.random_solution()
            self.population.append(individual)

    def random_solution(self):
        '''
        Generate a random solution without overlapping, favoring certain biscuit types based on heuristic.

        Returns:
        - individual (list): A list representing a possible solution (position, biscuit_type).
        '''
        biscuit_types_list = [3, 3, 3, 3, 0, 0, 1, 1, 2]  # Heuristic to favor certain biscuits
        individual = []
        position = 0
        while position < self.dough.LENGTH:
            random.shuffle(biscuit_types_list)  # Shuffle to introduce randomness
            for biscuit_type in biscuit_types_list:
                biscuit = self.biscuits[biscuit_type]
                if position + biscuit.length <= self.dough.LENGTH:
                    # Check defects in the dough segment
                    defects = self.dough.count_defects(position, biscuit.length)
                    # Verify if biscuit meets defect constraints
                    if all(defects.get(cls, 0) <= biscuit.max_defects[cls] for cls in biscuit.max_defects):
                        individual.append((position, biscuit_type))
                        position += biscuit.length
                        break
            else:
                # No biscuit could be placed; move to the next position
                position += 1
        return individual

    def fitness(self, individual):
        '''
        Calculate the fitness value of an individual solution, including penalty for unused dough.

        Parameters:
        - individual (list): A list representing an individual solution (list of tuples: (position, biscuit_type)).

        Returns:
        - total_value (float): The fitness value of the solution. Returns negative infinity for invalid solutions.
        '''
        total_value = 0
        occupied_positions = set()

        for position, biscuit_type in individual:
            biscuit = self.biscuits[biscuit_type]
            end_position = position + biscuit.length

            # Check if biscuit is within the dough
            if end_position > self.dough.LENGTH:
                return float('-inf')  # Invalid solution due to exceeding dough length

            # Check for overlapping
            biscuit_range = set(range(position, end_position))
            if occupied_positions.intersection(biscuit_range):
                return float('-inf')  # Invalid solution due to overlapping
            occupied_positions.update(biscuit_range)

            # Check defects
            defects = self.dough.count_defects(position, biscuit.length)
            if all(defects.get(cls, 0) <= biscuit.max_defects[cls] for cls in biscuit.max_defects):
                total_value += biscuit.value
            else:
                return float('-inf')  # Invalid solution due to defects exceeding maximum

        # Calculate penalty for unused positions
        total_positions = set(range(self.dough.LENGTH))
        unused_positions = total_positions - occupied_positions
        penalty = -len(unused_positions)
        total_value += penalty  # Subtract penalty from total value

        return total_value

    def selection(self):
        '''
        Perform roulette wheel selection to choose an individual from the population.

        Returns:
        - selected_individual (list): The selected individual from the population.
        '''
        fitness_values = [self.fitness(individual) for individual in self.population]
        total_fitness = sum(fitness_values)

        if total_fitness == 0:
            # All individuals are invalid; return a random individual
            return random.choice(self.population)

        pick = random.uniform(0, total_fitness)
        current = 0
        for individual, fitness_value in zip(self.population, fitness_values):
            current += fitness_value
            if current > pick:
                return individual

    @staticmethod
    def crossover(parent1, parent2):
        '''
        Perform one-point crossover on two parents to produce offspring without overlapping.

        Parameters:
        - parent1 (list): The first parent individual.
        - parent2 (list): The second parent individual.

        Returns:
        - tuple: Two offspring individuals.
        '''
        def create_child(p1, p2):
            child = []
            positions = set()
            i = j = 0
            len_p1, len_p2 = len(p1), len(p2)

            # Alternate genes from parents while avoiding overlapping
            while i < len_p1 or j < len_p2:
                if i < len_p1:
                    gene = p1[i]
                    biscuit_length = Biscuit(gene[1]).length
                    biscuit_positions = range(gene[0], gene[0] + biscuit_length)
                    if not positions.intersection(biscuit_positions):
                        child.append(gene)
                        positions.update(biscuit_positions)
                    i += 1
                if j < len_p2:
                    gene = p2[j]
                    biscuit_length = Biscuit(gene[1]).length
                    biscuit_positions = range(gene[0], gene[0] + biscuit_length)
                    if not positions.intersection(biscuit_positions):
                        child.append(gene)
                        positions.update(biscuit_positions)
                    j += 1
            return child

        child1 = create_child(parent1, parent2)
        child2 = create_child(parent2, parent1)

        return child1, child2

    def mutate(self, individual):
        '''
        Apply mutation to an individual while avoiding overlapping.

        Parameters:
        - individual (list): The individual to mutate.

        Returns:
        - individual (list): Mutated individual.
        '''
        if len(individual) > 0 and random.random() < self.mutation_rate:
            mutate_index = random.randint(0, len(individual) - 1)
            biscuit_positions = set()
            for idx, (pos, b_type) in enumerate(individual):
                if idx != mutate_index:
                    biscuit = self.biscuits[b_type]
                    biscuit_positions.update(range(pos, pos + biscuit.length))

            # Attempt to mutate the biscuit type or position without overlapping
            position, biscuit_type = individual[mutate_index]
            biscuit = self.biscuits[biscuit_type]

            if random.random() > 0.5:
                # Change biscuit type
                new_biscuit_type = random.choice(list(self.biscuits.keys()))
                new_biscuit = self.biscuits[new_biscuit_type]
                end_position = position + new_biscuit.length
                if end_position <= self.dough.LENGTH and not any(pos in biscuit_positions for pos in range(position, end_position)):
                    individual[mutate_index] = (position, new_biscuit_type)
            else:
                # Change position
                shift = random.choice([-1, 1])
                new_position = position + shift
                new_position = max(0, min(self.dough.LENGTH - biscuit.length, new_position))
                end_position = new_position + biscuit.length
                if not any(pos in biscuit_positions for pos in range(new_position, end_position)):
                    individual[mutate_index] = (new_position, biscuit_type)
        return individual

    def evolve(self):
        '''
        Evolve the population over one generation.
        '''
        new_population = []
        while len(new_population) < self.population_size:
            parent1 = self.selection()
            parent2 = self.selection()

            if random.random() < self.crossover_rate:
                offspring1, offspring2 = self.crossover(parent1, parent2)
            else:
                offspring1, offspring2 = parent1.copy(), parent2.copy()

            offspring1 = self.mutate(offspring1)
            offspring2 = self.mutate(offspring2)

            new_population.extend([offspring1, offspring2])

        self.population = new_population[:self.population_size]
