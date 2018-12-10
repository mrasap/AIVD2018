import math

from src.config import *
from src.bruteforce import *
from src.spellchecker.spellchecker import Spellchecker
from src.spellchecker.weeder import Weeder
import random
import matplotlib.pyplot as plt
from operator import itemgetter


class EvolutionaryStrategy:
    """
    The pydoc refers to slide 31 (genetic algorithm recap) from lecture 5.
    """

    def __init__(self,
            blueprint: [[str]],
            fitness_func=Weeder(Spellchecker()),
            path=PATH,
            pop_size=POP_SIZE,
            save_when_fitness_over=SAVE_WHEN_FITNESS_OVER,
    ):
        """
        :param blueprint: the matrix with all possibilities
        :param fitness_func: the fitness function that is applied, should have a compute(list) func.
        :param path: the path that we are following
        :param pop_size: the amount of chromosomes of the pop_selected.
                Note: given that chromosomes always offspring, the size of the total population
                is 2 * pop_size
        """
        self.generation = 0
        self.blueprint = blueprint
        self.path = path
        self.pop_size = pop_size
        self.fitness_func = fitness_func

        self.pop = self.generate_random_population(
            self.pop_size,
            blueprint
        )

        self.pop_fitness = []
        self.roulette_wheel = []
        self.pop_selected = []

        # These variables are used to track the performance of the GA during the training process
        self.average_fitness_over_generations = []
        self.best_fitness_over_generations = []
        self.mutate_rate_over_generations = []

        # Used to save all best results
        self.save_when_fitness_over = save_when_fitness_over
        self.best_chromosomes_strings_set = set()

    def generate_random_population(s, pop_size, blueprint):
        """
        Step 1 and 3: encoding and random initial population

        Start with a randomly sampled population of chromosomes.
        """
        pop = []
        for _ in range(pop_size * 2):
            chromosome = []
            for row in blueprint:
                row_blueprint = random.choice(row)
                chromosome.append(s.shuffle_knuth_yates(row_blueprint))
            pop.append(chromosome)
        return pop

    def fitness_function(s, chromosome):
        """
        Step 2: get the fitness function from the particular chromosome.

        This should be the inverse of the length of the path.

        :param chromosome: the tested chromosome
        :return: the fitness of the chromosome
        """
        line = strMatrixToString(chromosome, s.path)

        result = s.fitness_func.compute_valid(line)
        if result > FITNESS_FUNC_LIMITS[0]:
            result += math.floor((result - 28) ** 1.7)

        if result > FITNESS_FUNC_LIMITS[1]:
            result += s.fitness_func.compute_sensible(line)

        return result

    def fitness_computation_on_population(s):
        """
        Step 4: compute fitness for all population.
        """
        s.pop_fitness = []

        for chromosome in s.pop:
            s.pop_fitness.append(s.fitness_function(chromosome))

    def create_roulette_wheel(s):
        """
        Step 5.1: Set the roulette wheel, which is a list of upper boundaries of the probability.
        """
        s.roulette_wheel = []

        upper_bound = 0
        sum_fitness = sum(s.pop_fitness)
        for fitness in s.pop_fitness:
            upper_bound += fitness / (sum_fitness if sum_fitness else 0.01)
            s.roulette_wheel.append(upper_bound)

    def select_chromosome_from_roulette_wheel(s):
        """
        Step 5.2: Spin the roulette wheel and get the selected chromosome.

        :return: the selected chromosome
        """
        p_chosen = random.random()
        lower_bound = 0
        for i, (chromosome, upper_bound) in enumerate(zip(s.pop, s.roulette_wheel)):
            if lower_bound <= p_chosen <= upper_bound:
                return chromosome
            else:
                lower_bound = upper_bound

    def select_chromosomes_from_roulette_wheel(s):
        """
        Step 5: Select the chromosomes from the roulette wheel.
        """
        s.pop_selected = []

        for _ in range(s.pop_size):
            s.pop_selected.append(s.select_chromosome_from_roulette_wheel())

    def crossover(s, mother: [[str]], father: [[str]]) -> [[str]]:
        """
        Step 6.
        :param mother:
        :param father:
        :return:
        """
        length = random.randint(1, len(mother) - 1)
        start = random.randint(0, len(mother) - 1 - length)
        child_chromosome = [None for _ in range(len(mother))]

        # set the genes from the mother
        for i in range(start, start + length):
            child_chromosome[i] = mother[i]

        # fill the chromosome with the genes from the father
        for i, gene in enumerate(child_chromosome):
            if not gene:
                child_chromosome[i] = father[i]

        return child_chromosome

    def generate_offspring(s, chromosome) -> list:
        """
        Step 6: mutation. Two options are given: mutating every gene, or every gene has a chance
        to mutate.

        :param chromosome: chromosome that should be mutated
        :return: mutated chromosome
        """

        if s.always_crossover or random.random() <= s.crossover_rate:
            partner = s.pop_selected[random.randint(0, len(s.pop_selected) - 1)]
            offspring = s.crossover(chromosome, partner)
        else:
            offspring = chromosome.copy()

        return s.mutate(offspring)

    def mutate(s, chromosome) -> [[str]]:
        """
        Mutate the chromosome. Loop over all genes and mutate.

        :param chromosome: chromosome that should be mutated
        :return: mutated chromosome
        """
        if s.always_mutate:
            for i, gene in enumerate(chromosome):
                chromosome[i] = s.shuffle_knuth_yates(gene)
        else:
            for i, gene in enumerate(chromosome):
                if random.random() <= s.mutate_rate_current:
                    chromosome[i] = s.shuffle_with_convergence(gene)
        return chromosome

    def shuffle_knuth_yates(s, gene) -> [str]:
        """
        Step 6a: Knuth-Yates shuffle, reordering a array randomly. Every gene gets mutated every
        generation.

        :param gene: gene that should be mutated
        :return: mutated gene
        """
        n = len(gene)
        gene_new = gene.copy()
        for i in range(n):
            r = i + int(random.uniform(0, 1) * (n - i))
            swap = gene_new[r]
            gene_new[r] = gene_new[i]
            gene_new[i] = swap
        return gene_new

    def shuffle_with_convergence(s, gene) -> [str]:
        """
        Step 6b: Uses Knuth-Yates shuffle, but the chance that a gene is mutated is dependent on
        a probability.
        This probability can increase over a range of values throughout generations.

        :param gene: gene that should be mutated
        :return: mutated gene
        """
        n = len(gene)
        gene_new = gene.copy()
        for i in range(n):
            if random.random() <= s.mutate_rate_current:
                r = i + int(random.uniform(0, 1) * (n - i))
                swap = gene_new[r]
                gene_new[r] = gene_new[i]
                gene_new[i] = swap
        return gene_new

    def generate_next_generation(s):
        """
        Step 7 + 8: put offspring into new population.

        This function replaces the old population with the new population.
        """
        s.pop = []

        for chromosome in s.pop_selected:
            s.pop.append(chromosome)  # parent
            s.pop.append(s.generate_offspring(chromosome))  # offspring

        # apply variable mutation rate
        if not s.always_mutate:
            s.mutate_rate_current = s.mutate_rate_range[0] + s.generation * s.mutate_rate_step_size
            if s.mutate_rate_current > 1:
                s.mutate_rate_current = 1

        # apply elitism
        if s.always_include_best:
            for chrom, _ in s.best_chromosomes_with_fitness[
                            :random.randrange(*s.include_best_range)]:
                if not s.pop.__contains__(chrom):
                    s.pop.append(chrom)

    def track_best_chromosomes(s):
        """
        Keeps track of the best chromosomes this far.
        """
        # TODO: this is n^2
        new_best = []
        for chromosome, fitness in zip(s.pop, s.pop_fitness):
            if not new_best.__contains__([chromosome, fitness]):
                new_best.append([chromosome, fitness])

        s.best_chromosomes_with_fitness = sorted(new_best, key=itemgetter(1), reverse=True)[
                                          :s.include_best_range[1]]

        if s.best_chromosomes_with_fitness[0][1] > s.best_chromosome_fitness:
            s.best_chromosome, s.best_chromosome_fitness = s.best_chromosomes_with_fitness[0]

            print('new best fitness', s.best_chromosome_fitness, ', chromosome',
                strMatrixToString(s.best_chromosome, s.path))

        for chromosome, fitness in s.best_chromosomes_with_fitness:
            if fitness < s.save_when_fitness_over:
                break
            s.best_chromosomes_strings_set.add(strMatrixToString(chromosome, s.path))

    def track_performance_over_generations(s):
        """
        Keeps track of the performance of the GA throughout the training process.
        """
        if len(s.pop_fitness) == 0:
            # safety check, this should never happen.
            # If the graph returns a 0 value, then you know something went wrong.
            s.average_fitness_over_generations.append(0)
        else:
            s.average_fitness_over_generations.append(sum(s.pop_fitness) / len(s.pop_fitness))
        s.best_fitness_over_generations.append(s.best_chromosome_fitness)

        if not s.always_mutate:
            s.mutate_rate_over_generations.append(s.mutate_rate_current)

    def train_one_generation(s):
        """
        Train the GA one generation.
        """
        s.fitness_computation_on_population()
        s.create_roulette_wheel()
        s.select_chromosomes_from_roulette_wheel()
        s.track_best_chromosomes()
        s.track_performance_over_generations()
        s.generate_next_generation()
        s.generation += 1

    def train(s,
            generations=GENERATIONS,
            always_include_best=ALWAYS_INCLUDE_BEST,
            include_best_range=INCLUDE_BEST_RANGE,
            always_crossover=ALWAYS_CROSSOVER,
            crossover_rate=CROSSOVER_RATE,
            always_mutate=ALWAYS_MUTATE,
            mutate_rate_range=MUTATE_RATE_RANGE):
        """
        Train the GA up until the maximum of generations.

        :param generations: Int, amount of generations it should evolve
        :param always_include_best: Boolean, if true: it will ensure that the best chromosome is
        always in the population.
                Note: applies to the population, it does not ensure that it is always selected.
                Note: this could cause the size of the population to increase by one.
        :param include_best_range: Int, amount of best samples included. Rate is variable with
        lower and upper bound.
                Note: Could range between 0 (no elitism) and population size (only elitism).
        :param always_crossover: Boolean, if true, will always crossover a gene.
        :param crossover_rate: Float between 0 and 1, indicates the chance that a chromosome will
        crossover.
        :param always_mutate: Boolean, if true, always mutate a gene.
                If not, a gene will mutate with a chance in the range of mutate_rate_range.
        :param mutate_rate_range: Tuple, the start mutate rate and finish mutate rate. The mutate
        rate defines the
                probability that a gene mutates.
                Note: Needs to be between 0 and 1.
        """
        # These variables are used to variate the chance of mutation
        if not ((0 <= mutate_rate_range[0] <= 1) and (0 <= mutate_rate_range[1] <= 1)):
            raise ValueError("mutate rate range should be between 0 and 1")
        s.always_mutate = always_mutate
        s.mutate_rate_range = mutate_rate_range
        s.mutate_rate_step_size = (mutate_rate_range[1] - mutate_rate_range[0]) / generations
        s.mutate_rate_current = s.mutate_rate_range[0]

        # These variables are used to variate the chance of crossover
        if (crossover_rate > 1) or (crossover_rate < 0):
            raise ValueError("Crossover rate should be between 0 and 1")
        s.always_crossover = always_crossover
        s.crossover_rate = crossover_rate

        # These variables are used to keep track of the best chromosome
        if include_best_range[1] > s.pop_size:
            raise ValueError("Amount of best chromosomes included should be between 1 and pop size")
        s.best_chromosome = []
        s.best_chromosome_fitness = 0
        s.best_chromosomes_with_fitness = []  # list of lists, each list contains the chromosome
        # and the fitness.
        s.always_include_best = always_include_best
        s.include_best_range = include_best_range

        for _ in range(generations):
            s.train_one_generation()

    def plot_performance_over_generations(s,
            title='Performance of the GA (above) and mutation rate (below) over generations',
            xlabel='Generations',
            ylabel='Fitness function'):
        """
        Plot the performance of the genetic algorithm throughout the generations.
        """
        x = [i for i in range(s.generation)]
        plt.figure(1)
        plt.subplot(211)
        plt.title(title)
        plt.plot(x, s.average_fitness_over_generations, 'r--', label='average')
        plt.plot(x, s.best_fitness_over_generations, 'b-', label='best')
        plt.legend(loc='upper left')
        plt.ylabel(ylabel)

        plt.subplot(212)
        plt.plot(
            x,
            s.mutate_rate_over_generations if not s.always_mutate else [1 for _ in range(len(x))],
            'r--',
            label='mutate rate'
        )
        plt.plot(
            x,
            [s.crossover_rate for _ in range(len(x))] if not s.always_crossover else [1 for _ in
                                                                                      range(
                                                                                          len(x))],
            'b--',
            label='crossover rate'
        )
        plt.legend(loc='lower left')
        plt.ylabel('mutation rate')
        plt.xlabel(xlabel)
        plt.show()


# Assignment 2.b
if __name__ == "__main__":

    # First, I bruteforce all the possible rows of letters, and store them in a matrix.
    # This matrix consists of a list of 8 rows, and each row consists of a list of all possible
    # combinations of letters.
    combinationOfLettersPerRow = []
    for row in ROWS:
        print("\nNew row:", row)
        r = []
        letters = modulo(row[1])
        for combination in bruteForceLetters(letters=letters, withDuplicates=WITH_DUPLICATES):
            if sumOfRow(combination) == row[0] and productOfRow(combination) == row[1]:
                # print(rowToLetters(combination))
                r.append(rowToLetters(combination))
        combinationOfLettersPerRow.append(r)

    ga = EvolutionaryStrategy(blueprint=combinationOfLettersPerRow)

    # run optimization
    try:
        ga.train()
    finally:
        ga.plot_performance_over_generations()

        print('Current best solutions of the final generation')
        for chromosome, fitness in ga.best_chromosomes_with_fitness:
            # get the optimal solution and write to file
            print('fitness', fitness, ', chromosome',
                strMatrixToString(chromosome, ga.path))

        print('Writing all solutions that are over', ga.save_when_fitness_over)
        writeSetToCsv(ga.best_chromosomes_strings_set)
