import random
from Biscuit import Biscuit
from GeneticAlgorithm import *

class UniformCrossoverGA(GeneticAlgorithm):
    '''
    Genetic Algorithm class that implements uniform crossover with tournament selection and elitism.
    Inherits from the base GeneticAlgorithm class.
    '''

    def __init__(self, dough, biscuits, population_size, mutation_rate, crossover_rate):
        '''
        Initialize the UniformCrossoverGA algorithm with the given parameters.

        Parameters:
        - dough: The Dough object representing the dough to place biscuits on.
        - biscuits: A dictionary of Biscuit objects indexed by their type.
        - population_size: The number of individuals in the population.
        - mutation_rate: The probability of mutation occurring.
        - crossover_rate: The probability of crossover occurring.
        '''
        super().__init__(dough, biscuits, population_size, mutation_rate, crossover_rate)
        self.tournament_size = 15  # Size of the tournament for selection

    def selection(self, elite_size):
        '''
        Perform selection using tournament selection and elitism.

        Parameters:
        - elite_size: The number of top individuals to automatically select (elitism).

        Returns:
        - selected_individuals: A list of selected individuals for the next generation.
        '''
        # Rank the population based on fitness
        ranked_population = [(individual, self.fitness(individual)) for individual in self.population]
        ranked_population.sort(key=lambda x: x[1], reverse=True)

        # Select elite individuals
        selected_individuals = [individual for individual, _ in ranked_population[:elite_size]]

        # Perform tournament selection for the rest of the population
        for _ in range(len(ranked_population) - elite_size):
            # Randomly select individuals for the tournament
            tournament = random.sample(ranked_population, self.tournament_size)
            # Select the best individual from the tournament
            best_individual = sorted(tournament, key=lambda x: x[1], reverse=True)[0][0]
            selected_individuals.append(best_individual)

        return selected_individuals

    @staticmethod
    def uniform_crossover(parent1, parent2, max_attempts=500):
        '''
        Perform uniform crossover on two parents to produce offspring without overlapping.

        Parameters:
        - parent1: The first parent individual.
        - parent2: The second parent individual.
        - max_attempts: Maximum number of attempts to find valid crossover points.

        Returns:
        - tuple: Two offspring individuals.
        '''
        # Define the biscuit types
        biscuits = {
            0: Biscuit(0),
            1: Biscuit(1),
            2: Biscuit(2),
            3: Biscuit(3),
            4: Biscuit(4)
        }

        def find_valid_crossover_points(parent):
            '''
            Find valid crossover points in a parent individual.

            Parameters:
            - parent: The parent individual.

            Returns:
            - valid_points: A list of valid crossover points (indices).
            '''
            valid_points = []
            for i in range(1, len(parent)):
                prev_position, prev_type = parent[i - 1]
                current_position, _ = parent[i]
                # Ensure there is space between biscuits to prevent overlapping
                if current_position - (prev_position + biscuits[prev_type].length) > 0:
                    valid_points.append(i)
            return valid_points

        def create_child(parent_a, parent_b, crossover_point):
            '''
            Create a child individual from two parents at a given crossover point.

            Parameters:
            - parent_a: The first parent individual.
            - parent_b: The second parent individual.
            - crossover_point: The index at which to perform crossover.

            Returns:
            - child: The resulting child individual.
            '''
            # Combine genes from both parents
            child = parent_a[:crossover_point] + [gene for gene in parent_b[crossover_point:] if gene not in parent_a[:crossover_point]]
            return child

        # Sort parents by position to maintain order
        parent1_sorted = sorted(parent1, key=lambda x: x[0])
        parent2_sorted = sorted(parent2, key=lambda x: x[0])

        for _ in range(max_attempts):
            valid_points_p1 = find_valid_crossover_points(parent1_sorted)
            valid_points_p2 = find_valid_crossover_points(parent2_sorted)

            if valid_points_p1 and valid_points_p2:
                # Randomly select crossover points from valid points
                crossover_point1 = random.choice(valid_points_p1)
                crossover_point2 = random.choice(valid_points_p2)

                # Create children using the selected crossover points
                child1 = create_child(parent1_sorted, parent2_sorted, crossover_point1)
                child2 = create_child(parent2_sorted, parent1_sorted, crossover_point2)

                return child1, child2

        # Return parents if no valid crossover point is found
        return parent1, parent2

    def evolve(self):
        '''
        Evolve the population over one generation using uniform crossover, tournament selection, and elitism.
        '''
        # Determine the number of elite individuals to carry over
        elite_size = int(self.population_size * 0.2)
        # Perform selection to get individuals for breeding
        selected_individuals = self.selection(elite_size)
        # Start the new population with elite individuals
        new_population = selected_individuals[:elite_size]

        # Generate the rest of the new population
        while len(new_population) < self.population_size:
            # Randomly select parents from the elite individuals
            parent1 = random.choice(selected_individuals[:elite_size])
            parent2 = random.choice(selected_individuals[:elite_size])
            # Perform uniform crossover to produce offspring
            child1, child2 = self.uniform_crossover(parent1, parent2)
            # Add offspring to the new population
            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)

        # Update the population with the new generation
        self.population = new_population
