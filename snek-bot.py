# Size of each population
POP_SIZE = 100

# Number of individuals from each generation to be selected for breeding
N_PROG = 10

'''
These values should follow the rule
POP_SIZE = N_PROG * 10*N_BATCH, for every integer N_BATCH '''

'''
Every pair of parents should result in 10*N_BATCH chromosomes,
as every crossover iteration generates 10 chromosomes '''
N_BATCH = int((POP_SIZE / N_PROG) / 10)

# Number of lucky chromosomes to be randomly selected for breeding,
# to maintain genetic variability
LUCKY_ONES = 0

# Number of generations
N_GEN = 20

# Mutation rate
MUT_RATE = 0.1

# Number of genes
N_GENES = 5

# Breeding method (either 'genetic', 'arithmetic', 'coinflip' or 'mixed')
BREEDING = 'genetic'

'''
	GENE BOUNDS
This are the lower (first value) and upper (second value) boundaries for
the random generation of genes, wich happens in the inicialization of the
first generation and in the event of mutation. '''

GENE1 = [20.000, 200.000]
GENE2 = [01.000, 10.000]
GENE3 = [1.0000, 2.0000]
GENE4 = [0.0010, 0.0020]
GENE5 = [-1.000, 01.000]


from bot import Bot
from game.bot_train import BotTrain
from game.bot_game import BotGame
from tweak.ga_tweak import *

from random import randint, uniform
import numpy as np
from math import *
import sys
from time import sleep

# generates random DNA (genome, dna, etc)


def gen_random_dna():
    return [uniform(GENE1[0], GENE1[1]),
            uniform(GENE2[0], GENE2[1]),
            uniform(GENE3[0], GENE3[1]),
            uniform(GENE4[0], GENE4[1]),
            uniform(GENE5[0], GENE5[1])]

# generates random population


def gen_random_population():
    pop = []
    for i in range(0, POP_SIZE):
        randDna = gen_random_dna()
        pop.append(Bot(randDna))

    return pop


'''
	various possible methods of chromosome crossover
'''


def genetic_crossover(dnaA, dnaB, elite, son):
    chromosome_A = []
    chromosome_B = []

    SPLIT = int(N_GENES / 2)

    chromosome_A[:SPLIT] = dnaA[:SPLIT]
    chromosome_A[SPLIT:N_GENES] = dnaB[SPLIT:N_GENES]

    chromosome_B[:SPLIT] = dnaB[:SPLIT]
    chromosome_B[SPLIT:N_GENES] = dnaA[SPLIT:N_GENES]

    # Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function)
    # Does not apply mutation if one of the parent dnas is the best one (elitism)
    if not elite:
        mutation(chromosome_A)
        mutation(chromosome_B)

    if son == 'A':
        return chromosome_A
    else:
        return chromosome_B


def arithmetic_crossover(dnaA, dnaB, elite, son):
    chromosome_A = []
    chromosome_B = []
    chromosome_C = []

    # Chromosome favoring parent A
    for i in range(N_GENES):
        chromosome_A.append(((3 * dnaA[i]) + (1 * dnaB[i])) / 4)

    # Chromosome favoring parent B
    for i in range(N_GENES):
        chromosome_B.append(((1 * dnaA[i]) + (3 * dnaB[i])) / 4)

    # Neutral dna
    for i in range(N_GENES):
        chromosome_C.append((dnaA[i] + dnaB[i]) / 2)

    # Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function)
    # Does not apply mutation if one of the parent dnas is the best one (elitism)
    if not elite:
        mutation(chromosome_A)
        mutation(chromosome_B)
        mutation(chromosome_C)

    if son == 'A':
        return chromosome_A
    elif son == 'B':
        return chromosome_B
    else:
        return chromosome_C


def coinflip_crossover(dnaA, dnaB, elite):
    chromo = []

    # Coin flip crossover
    for i in range(N_GENES):
        if randint(0, 1) == 0:
            chromo.append(dnaA[i])
        else:
            chromo.append(dnaB[i])

    # Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function).
    # Does not apply mutation if one of the parent dnas is the best one (elitism)
    if not elite:
        mutation(chromo)

    return chromo


def mutation(dna):
    # Every gene of the dna has the chance to mutate
    for i in range(0, N_GENES):

        mut = uniform(0.0, 1.0)
        if mut <= MUT_RATE:
            # We need to keep track of the upper and lower bounds for each gene
            if i == 0:
                dna[i] = uniform(GENE1[0], GENE1[1])
            elif i == 1:
                dna[i] = uniform(GENE2[0], GENE2[1])
            elif i == 2:
                dna[i] = uniform(GENE3[0], GENE3[1])
            elif i == 3:
                dna[i] = uniform(GENE4[0], GENE4[1])
            elif i == 4:
                dna[i] = uniform(GENE5[0], GENE5[1])


def breeding(parentA, parentB, elite):
    # Generates 10 dnas based on the chosen breeding method
    offspring = []

    if BREEDING == 'genetic':
        # 5x the two possible combinations from genetic crossover
        for k in range(5):
            offspring.append(Bot(genetic_crossover(
                parentA.dna, parentB.dna, elite, 'A')))
            offspring.append(Bot(genetic_crossover(
                parentA.dna, parentB.dna, elite, 'B')))

    elif BREEDING == 'arithmetic':
        # 3x the three possible combinations from arithmetic crossover
        for k in range(3):
            offspring.append(Bot(arithmetic_crossover(
                parentA.dna, parentB.dna, elite, 'A')))
            offspring.append(Bot(arithmetic_crossover(
                parentA.dna, parentB.dna, elite, 'B')))
            offspring.append(Bot(arithmetic_crossover(
                parentA.dna, parentB.dna, elite, 'C')))
        offspring.append(Bot(arithmetic_crossover(
            parentA.dna, parentB.dna, elite, 'C')))

    elif BREEDING == 'coinflip':
        # Ten random combinations from coinflip crossover
        for k in range(10):
            offspring.append(Bot(coinflip_crossover(
                parentA.dna, parentB.dna, elite)))

    elif BREEDING == 'mixed':
        # Two possible combinations from genetic crossover
        offspring.append(Bot(genetic_crossover(
            parentA.dna, parentB.dna, elite, 'A')))
        offspring.append(Bot(genetic_crossover(
            parentA.dna, parentB.dna, elite, 'B')))

        # Three possible combinations from arithmetic crossover
        offspring.append(Bot(arithmetic_crossover(
            parentA.dna, parentB.dna, elite, 'A')))
        offspring.append(Bot(arithmetic_crossover(
            parentA.dna, parentB.dna, elite, 'B')))
        offspring.append(Bot(arithmetic_crossover(
            parentA.dna, parentB.dna, elite, 'C')))

        # Five random combinations from coinflip crossover
        for k in range(5):
            offspring.append(Bot(coinflip_crossover(
                parentA.dna, parentB.dna, elite)))

    return offspring

# Gives birth to a whole new generation


def new_generation(progenitors):
    newPop = []

    '''
		every breeding execution generates 10 dnas. Thus, N_BATCH comes to action
	'''

    # This loop breeds all except one pair of parents (i with i+1)
    for i in range(0, N_PROG - 1):

        # Applying elitism (protection of best dna against mutation)
        if i == 0:
            elite = True
        else:
            elite = False

        for j in range(N_BATCH):
            offspring = breeding(progenitors[i], progenitors[i + 1], elite)
            newPop.extend(offspring)

    # Last pair of parents (0 and the last one)
    for j in range(N_BATCH):
        offspring = breeding(progenitors[0], progenitors[N_PROG - 1], True)
        newPop.extend(offspring)

    return newPop


if __name__ == '__main__':
    # Generating the first (random) population
    population = gen_random_population()

    # Loops for each generation
    for n in range(1, N_GEN + 1):

        print("----------------------------------------")
        print("Generation", n, ":")

        # Evaluation (population plays the game and their fitness score is set)
        for i in range(0, POP_SIZE):

            training = BotTrain(population[i])
            training.play()

            print("Gen", n, "\tIndiv.", i, "fitness:", population[i].fitness)

        # Selection (individuals are sorted based on their fitness score, the first PROG individuals are selected as progenitors)
        population.sort(key=lambda i: i.fitness, reverse=True)
        progenitors = population[:N_PROG - LUCKY_ONES]

        # Selects a number of lucky ones (random dnas from the population), for the sake of genetic variability
        for i in range(0, LUCKY_ONES):
            progenitors.append(population[randint(0, POP_SIZE - 1)])

        # Output of generation progenitors
        print("----------------------------------------")
        print("Gen", n, "\tBest fit:")
        avgFit = 0
        for i in range(0, len(progenitors)):
            print('\t', i + 1, ':', progenitors[i].fitness)
            avgFit += progenitors[i].fitness

        avgFit = avgFit / POP_SIZE
        print("\nAverage fitness:", avgFit)
        print("----------------------------------------")

        # Gives birth to a new generation, based on the genes generated from crossover and mutation
        population = new_generation(progenitors)

        # Best dna of this generations gets the chance to show its abilities
        print("This generation best individual showoff:")
        print("Press ENTER to end...")
        genShowoff = BotGame(progenitors[0], n)
        genShowoff.play()

    input('Training is complete. Press ENTER to watch the best dna play the game.')

    # Visualize the best of the best
    overallShowoff = BotGame(progenitors[0], n)
    overallShowoff.play()
