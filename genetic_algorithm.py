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
from tweak.ga_tweak import *

# Generates random population
def randPopulation():
	pop = []
	for i in range(0, POP_SIZE):
		randChromo =   [uniform(GENE1[0], GENE1[1]),
						uniform(GENE2[0], GENE2[1]),
						uniform(GENE3[0], GENE3[1]),
						uniform(GENE4[0], GENE4[1]),
						uniform(GENE5[0], GENE5[1])]

		pop.append(Individual(randChromo))

	return pop

'''
There are various possible methods of genetic crossover of cromosomes.
For the sake of ease of exeperimentation, I implemented some.
'''
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

def coinflipCrossover(chromosomeA, chromosomeB, elite):
	chromoSon = []

	# Coin flip crossover
	for i in range(N_GENES):
		if randint(0, 1) == 0:
			chromoSon.append(chromosomeA[i])
		else:
			chromoSon.append(chromosomeB[i])

	# Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function).
	# Does not apply mutation if one of the parent chromosomes is the best one (elitism)
	if not elite:
		mutation(chromoSon)

	return chromoSon

def mutation(chromosome):
	# Every gene of the chromosome has the chance to mutate
	for i in range(0, N_GENES):

		mut = uniform(0.0, 1.0)
		if mut <= MUT_RATE:

			# We need to keep track of the upper and lower bounds for each gene
			if i == 0:
				chromosome[i] = uniform(GENE1[0], GENE1[1])
			elif i == 1:
				chromosome[i] = uniform(GENE2[0], GENE2[1])
			elif i == 2:
				chromosome[i] = uniform(GENE3[0], GENE3[1])
			elif i == 3:
				chromosome[i] = uniform(GENE4[0], GENE4[1])
			elif i == 4:
				chromosome[i] = uniform(GENE5[0], GENE5[1])

def breeding(parentA, parentB, elite):
	# Generates 10 chromosomes based on the chosen breeding method
	offspring = []

	if BREEDING == 'genetic':
		# 5x the two possible combinations from genetic crossover
		for k in range(5):
			offspring.append( Individual( geneticCrossover(parentA.chromosome, parentB.chromosome, elite, 'A')    ))
			offspring.append( Individual( geneticCrossover(parentA.chromosome, parentB.chromosome, elite, 'B')    ))
		
	elif BREEDING == 'arithmetic':
		# 3x the three possible combinations from arithmetic crossover
		for k in range(3):
			offspring.append( Individual( arithmeticCrossover(parentA.chromosome, parentB.chromosome, elite, 'A') ))
			offspring.append( Individual( arithmeticCrossover(parentA.chromosome, parentB.chromosome, elite, 'B') ))
			offspring.append( Individual( arithmeticCrossover(parentA.chromosome, parentB.chromosome, elite, 'C') ))
		offspring.append( Individual( arithmeticCrossover(parentA.chromosome, parentB.chromosome, elite, 'C') ))

	elif BREEDING == 'coinflip':
		# Ten random combinations from coinflip crossover
		for k in range(10):
			offspring.append( Individual( coinflipCrossover(parentA.chromosome, parentB.chromosome, elite)    ))

	elif BREEDING == 'mixed':
		# Two possible combinations from genetic crossover
		offspring.append( Individual( geneticCrossover(parentA.chromosome, parentB.chromosome, elite, 'A')    ))
		offspring.append( Individual( geneticCrossover(parentA.chromosome, parentB.chromosome, elite, 'B')    ))

		# Three possible combinations from arithmetic crossover
		offspring.append( Individual( arithmeticCrossover(parentA.chromosome, parentB.chromosome, elite, 'A') ))
		offspring.append( Individual( arithmeticCrossover(parentA.chromosome, parentB.chromosome, elite, 'B') ))
		offspring.append( Individual( arithmeticCrossover(parentA.chromosome, parentB.chromosome, elite, 'C') ))

		# Five random combinations from coinflip crossover
		for k in range(5):
			offspring.append( Individual( coinflipCrossover(parentA.chromosome, parentB.chromosome, elite)    ))

	return offspring

# Gives birth to a whole new generation
def newGen(progenitors):
	newPop = []

	'''
	Every breeding execution generates 10 chromosomes. Thus, N_BATCH comes to actionS
	'''

	# This loop breeds all except one pair of parents (i with i+1)
	for i in range(0, N_PROG-1):
		
		# Applying elitism (protection of best chromosome against mutation)
		if i == 0:
			elite = True
		else:
			elite = False

		for j in range(N_BATCH):
			offspring = breeding(progenitors[i], progenitors[i+1], elite)
			newPop.extend(offspring)

	# Last pair of parents (0 and the last one)
	for j in range(N_BATCH):
		offspring = breeding(progenitors[0], progenitors[N_PROG-1], True)
		newPop.extend(offspring)

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

		# Selection (individuals are sorted based on their fitness score, the first PROG individuals are selected as progenitors)
		population.sort(key=lambda i:i.fitness, reverse = True)
		progenitors = population[:N_PROG-LUCKY_ONES]

		# Selects a number of lucky ones (random chromosomes from the population), for the sake of genetic variability
		for i in range(0, LUCKY_ONES):
			progenitors.append( population[randint(0, POP_SIZE-1)] )

		# Output of generation progenitors
		print("----------------------------------------")
		print("Gen", n,"\tBest fit:")
		avgFit = 0
		for i in range(0, len(progenitors)):
			print('\t', i+1, ':', progenitors[i].fitness)
			avgFit += progenitors[i].fitness

		avgFit = avgFit/POP_SIZE
		print("\nAverage fitness:", avgFit)
		print("----------------------------------------")

		# Gives birth to a new generation, based on the genes generated from crossover and mutation
		population = newGen(progenitors)

		# Best chromosome of this generations gets the chance to show its abilities
		visualization.play( progenitors[0].chromosome, n)

	input('Training is complete. Press ENTER to watch the best chromosome play the game.')
	# Visualize the best of the best
	visualization.play( progenitors[0].chromosome, n)