#!/usr/bin/python3

'''
This is the code related to the genetic algorithm itself, as the main controller of everything that's going on.

This is the main file and is the one that should be executed.
'''

import game_training as training
import game_visualization as visualization
from bot import Individual

from random import randint, uniform
import numpy as np
from math import *
import sys
from time import sleep

#############################################################################
#								# CONSTANTS #										

# Size of each population
POP_SIZE = 100

# Number of individuals from each generation to be selected for breeding (progenitors)
N_PROG = 10

# Number of lucky chromosomes to be selected for breeding (to maintain genetic variability)
LUCKY_ONES = 0

# Number of sons by each pair of parents
N_SONS = int(POP_SIZE/N_PROG)

# Number of generations
N_GEN = 100

# Mutation rate
MUT_RATE = 0.10

# Number of genes (this can't be tweaked without making other changes to the code)
N_GENES = 5

#############################################################################

# Generates random population
def randPopulation():
	pop = []
	for i in range(0, POP_SIZE):
		randChromo =   [uniform(3.0, 99.0),
						uniform(0.01, 2.0),
						uniform(3.0, 99.0),
						uniform(-1.0, 1.0),
						uniform(0.01, 1.0)]

		pop.append(Individual(randChromo))

	return pop

'''
There are various possible methods of genetic crossover of cromosomes.
For the sake of ease of exeperimentation, I implemented some
'''

# Genetic crossover. Returns 2 sons.
def geneticCrossover(chromosomeA, chromosomeB, elite, son):
	chromoSonA = []
	chromoSonB = []

	SPLIT = int(N_GENES/2)

	chromoSonA[:SPLIT] = chromosomeA[:SPLIT]
	chromoSonA[SPLIT:N_GENES] = chromosomeB[SPLIT:N_GENES]

	chromoSonB[:SPLIT] = chromosomeB[:SPLIT]
	chromoSonB[SPLIT:N_GENES] = chromosomeA[SPLIT:N_GENES]

	# Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function)
	# Does not apply mutation if one of the parent chromosomes is the best one (elitism)
	if not elite:
		mutation(chromoSonA)
		mutation(chromoSonB)
	
	if son == 'A':
		return chromoSonA
	else:
		return chromoSonB	

# Arithmetic crossover. Returns 3 sons (one favoring each parent and one 'neutral')
def arithmeticCrossover(chromosomeA, chromosomeB, elite, son):
	chromoSonA = []
	chromoSonB = []
	chromoSonC = []

	# Chromosome favoring parent A
	for i in range(N_GENES):
		chromoSonA.append( ((3*chromosomeA[i]) + (1*chromosomeB[i])) / 4 )

	# Chromosome favoring parent B
	for i in range(N_GENES):
		chromoSonB.append( ((1*chromosomeA[i]) + (3*chromosomeB[i])) / 4 )

	# Neutral chromosome
	for i in range(N_GENES):
		chromoSonC.append( (chromosomeA[i]+chromosomeB[i]) / 2 )

	# Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function)
	# Does not apply mutation if one of the parent chromosomes is the best one (elitism)
	if not elite:
		mutation(chromoSonA)
		mutation(chromoSonB)
		mutation(chromoSonC)

	if son == 'A':
		return chromoSonA
	elif son == 'B':
		return chromoSonB	
	else:
		return chromoSonC

# Coin-flip crossover. Returns only one son
def coinflipCrossover(chromosomeA, chromosomeB, elite):
	chromoSon = []

	# Coin flip crossover
	for i in range(N_GENES):
		if randint(0, 1) == 0:
			chromoSon.append(chromosomeA[i])
		else:
			chromoSon.append(chromosomeB[i])

	# Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function)
	# Does not apply mutation if one of the parent chromosomes is the best one (elitism)
	if not elite:
		mutation(chromoSon)

	return chromoSon

# Chromosome mutation
def mutation(chromosome):

	# Every gene of the chromosome has the chance to mutate
	for i in range(0, N_GENES):

		mut = uniform(0.0, 1.0)
		if mut <= MUT_RATE:

			# We need to keep track of the upper and lower bounds for each gene
			if i == 0:
				chromosome[i] = uniform(3.0, 99.0)
			elif i == 1:
				chromosome[i] = uniform(0.01, 2.0)
			elif i == 2:
				chromosome[i] = uniform(3.0, 99.0)
			elif i == 3:
				chromosome[i] = uniform(-1.0, 1.0)
			elif i == 4:
				chromosome[i] = uniform(0.01, 1.0)

# Gives birth to a whole new generation
def newGen(progenitors):
	newPop = []

	# Each parent combination should produce N_SONS chromosomes as each generation should have POP_SIZE individuals 

	# genetic = 2, arithmetic = 3, coin-flip = 1. N_SONS = 10

	for i in range(0, N_PROG-1):
		
		# Applying elitism (protection of best chromosome against mutation)
		if i == 0:
			elite = True
		else:
			elite = False

		for j in range(1):

			# Generating 10 chromosomes:

			# Genetic crossover:
			for k in range(5):
				newPop.append( Individual( geneticCrossover(progenitors[i].chromosome, progenitors[i+1].chromosome, elite, 'A')    )) # 1
				newPop.append( Individual( geneticCrossover(progenitors[i].chromosome, progenitors[i+1].chromosome, elite, 'B')    )) # 1

			# Arithmetic crossover:
			for k in range(3):
				newPop.append( Individual( arithmeticCrossover(progenitors[i].chromosome, progenitors[i+1].chromosome, elite, 'A') )) # 1
				newPop.append( Individual( arithmeticCrossover(progenitors[i].chromosome, progenitors[i+1].chromosome, elite, 'B') )) # 1
				newPop.append( Individual( arithmeticCrossover(progenitors[i].chromosome, progenitors[i+1].chromosome, elite, 'C') )) # 1
			newPop.append( Individual( arithmeticCrossover(progenitors[i].chromosome, progenitors[i+1].chromosome, elite, 'C') )) # 1
			
			# Coinflip crossover:		
			# for k in range(10):
			# 	newPop.append( Individual( coinflipCrossover(progenitors[i].chromosome, progenitors[i+1].chromosome, elite)    )) # 1

	elite = True

	for j in range(1):

		# Generates 10 chromosomes:

		# # Genetic crossover:
		# for k in range(5):		for k in range(5):
		# 	newPop.append( Individual( geneticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'A')    )) # 1
		# 	newPop.append( Individual( geneticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'B')    )) # 1

		# 	newPop.append( Individual( geneticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'A')    )) # 1
		# 	newPop.append( Individual( geneticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'B')    )) # 1
		
		# Arithmetic crossover:
		for k in range(3):
			newPop.append( Individual( arithmeticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'A') )) # 1
			newPop.append( Individual( arithmeticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'B') )) # 1
			newPop.append( Individual( arithmeticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'C') )) # 1
		newPop.append( Individual( arithmeticCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite, 'C') )) # 1

		# Coinflip crossover:
		# for k in range(10):
			# newPop.append( Individual( coinflipCrossover(progenitors[0].chromosome, progenitors[N_PROG-1].chromosome, elite)    )) # 1

	return newPop


if __name__ == '__main__':

	# Generating the first (random) population
	population = randPopulation()

	# Loops for each generation
	for n in range(1, N_GEN+1):
		
		print("----------------------------------------")
		print("Generation", n, ":")

		# Evaluation (population plays the game and their fitness score is set)
		for i in range(0, POP_SIZE):

			training.Evaluate(population[i])
			print("Gen", n,"\tIndiv.", i, "fitness:", population[i].fitness)

			# Visualizing this individual
			# visualization.play(population[i].chromosome, n)


		# Selection (individuals are sorted based on their fitness score, the first PROG individuals are selected as progenitors)
		population.sort(key=lambda i:i.fitness, reverse = True)
		progenitors = population[:N_PROG-LUCKY_ONES]

		# Selects a number of lucky ones (random chromosomes from the population), for the sake of genetic variability
		for i in range(0, LUCKY_ONES):
			progenitors.append( population[randint(0, POP_SIZE-1)] )

		# Output of generation progenitors
		print("----------------------------------------")
		print("Gen", n,"\tBest fit:")
		for i in range(0, len(progenitors)):
			print('\t', i+1, ':', progenitors[i].fitness)
		print("----------------------------------------")

		# Gives birth to a new generation, based on the genes generated from crossover and mutation
		population = newGen(progenitors)

		# This generations best chromosome gets the chance to show its abilities
		visualization.play( progenitors[0].chromosome, n)

	input('a')
	# Visualize the best of the best
	visualization.play( progenitors[0].chromosome, n)