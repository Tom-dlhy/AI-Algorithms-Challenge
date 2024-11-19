import random
from GeneticAlgorithm import *
from Biscuit import *

class GeneticElitism(GeneticAlgorithm):
    '''
    Genetic Algorithm class implementing elitism in the selection process.
    Inherits from the base GeneticAlgorithm class.
    '''
    def __init__(self, dough, biscuits, population_size, mutation_rate, crossover_rate):
        '''
        Initialize the GeneticElitism algorithm with the given parameters.

        Parameters:
        - dough: The Dough object representing the dough to place biscuits on.
        - biscuits: A dictionary of Biscuit objects indexed by their type.
        - population_size: The number of individuals in the population.
        - mutation_rate: The probability of mutation occurring.
        - crossover_rate: The probability of crossover occurring.
        '''
        # Call the initializer of the parent class GeneticAlgorithm
        super().__init__(dough, biscuits, population_size, mutation_rate, crossover_rate)

    def selection(self):
        '''
        Perform selection using roulette wheel selection with elitism.

        This method calculates the cumulative fitness of the population,
        picks a random value between 0 and the total fitness,
        and iterates through the population summing fitness values
        until the cumulative fitness exceeds the random value.
        The individual at that point is selected.

        Returns:
        - selected_individuals: A list of selected individuals for the next generation.
        '''
        # Calculate the total fitness of the population
        total_fitness = sum(self.fitness(individual) for individual in self.population)

        # Create a list to hold selected individuals
        selected_individuals = []

        # Number of elite individuals to carry over
        elite_size = int(self.population_size * 0.2)
        # Sort the population based on fitness in descending order
        ranked_population = sorted(self.population, key=lambda ind: self.fitness(ind), reverse=True)
        # Add elite individuals to the selected list
        selected_individuals.extend(ranked_population[:elite_size])

        # Perform roulette wheel selection for the rest of the population
        for _ in range(self.population_size - elite_size):
            pick = random.uniform(0, total_fitness)
            current = 0
            for individual in self.population:
                current += self.fitness(individual)
                if current > pick:
                    selected_individuals.append(individual)
                    break

        return selected_individuals

    def mutate(self, individual, mutation_rate):
        '''
        Apply mutation to an individual.

        Parameters:
        - individual: The individual to mutate.
        - mutation_rate: The probability of mutation at each position.

        Returns:
        - The mutated individual.
        '''
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                # Select a random position to swap with
                swap_with = random.randint(0, len(individual) - 1)
                # Swap the positions
                individual[i], individual[swap_with] = individual[swap_with], individual[i]
        return individual

    def mutate_population(self, population):
        '''
        Apply mutation to the entire population.

        Parameters:
        - population: The population to mutate.

        Returns:
        - The mutated population.
        '''
        return [self.mutate(individual, self.mutation_rate) for individual in population]

    def evolve(self):
        '''
        Evolve the population over one generation using elitism, crossover, and mutation.
        '''
        # Perform selection to get individuals for breeding
        selected_individuals = self.selection()
        # Start the new population with elite individuals
        elite_size = int(self.population_size * 0.2)
        new_population = selected_individuals[:elite_size]

        # Generate offspring through crossover
        offspring_population = []

        for i in range(elite_size, self.population_size, 2):
            parent1 = selected_individuals[i % len(selected_individuals)]
            parent2 = selected_individuals[(i + 1) % len(selected_individuals)]
            # Perform crossover to produce children
            child1, child2 = GeneticAlgorithm.crossover(parent1, parent2)
            offspring_population.append(child1)
            # Ensure offspring list doesn't exceed required size
            if len(offspring_population) < self.population_size - elite_size:
                offspring_population.append(child2)

        # Apply mutation to offspring
        mutated_offspring = self.mutate_population(offspring_population)

        # Combine elite individuals and mutated offspring to form new population
        self.population = new_population + mutated_offspring

    def fitness(self, individual):
        '''
        Calculate the fitness value of an individual solution, including penalty for unused dough.

        Parameters:
        - individual: A list representing an individual solution (list of tuples: (position, biscuit_type)).

        Returns:
        - The fitness value of the solution. Returns negative infinity for invalid solutions.
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
