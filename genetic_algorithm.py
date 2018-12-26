#!/usr/bin/python3

'''
This is the code related to the genetic algorithm itself, as the main controller of everything that's going on.

This is the main file and is the one that should be executed.
'''

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
def genRandDna():
	return [uniform(GENE1[0], GENE1[1]),
			uniform(GENE2[0], GENE2[1]),
			uniform(GENE3[0], GENE3[1]),
			uniform(GENE4[0], GENE4[1]),
			uniform(GENE5[0], GENE5[1])]

# generates random population
def genRandPopulation():
	pop = []
	for i in range(0, POP_SIZE):
		randDna = genRandDna();
		pop.append(Bot(randDna))

	return pop

'''
There are various possible methods of genetic crossover of cromosomes.
For the sake of ease of exeperimentation, there is a function for eatch method.
'''
def geneticCrossover(dnaA, dnaB, elite, son):
	chromoSonA = []
	chromoSonB = []

	SPLIT = int(N_GENES/2)

	chromoSonA[:SPLIT] = dnaA[:SPLIT]
	chromoSonA[SPLIT:N_GENES] = dnaB[SPLIT:N_GENES]

	chromoSonB[:SPLIT] = dnaB[:SPLIT]
	chromoSonB[SPLIT:N_GENES] = dnaA[SPLIT:N_GENES]

	# Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function)
	# Does not apply mutation if one of the parent dnas is the best one (elitism)
	if not elite:
		mutation(chromoSonA)
		mutation(chromoSonB)
	
	if son == 'A':
		return chromoSonA
	else:
		return chromoSonB	

def arithmeticCrossover(dnaA, dnaB, elite, son):
	chromoSonA = []
	chromoSonB = []
	chromoSonC = []

	# Chromosome favoring parent A
	for i in range(N_GENES):
		chromoSonA.append( ((3*dnaA[i]) + (1*dnaB[i])) / 4 )

	# Chromosome favoring parent B
	for i in range(N_GENES):
		chromoSonB.append( ((1*dnaA[i]) + (3*dnaB[i])) / 4 )

	# Neutral dna
	for i in range(N_GENES):
		chromoSonC.append( (dnaA[i]+dnaB[i]) / 2 )

	# Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function)
	# Does not apply mutation if one of the parent dnas is the best one (elitism)
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

def coinflipCrossover(dnaA, dnaB, elite):
	chromoSon = []

	# Coin flip crossover
	for i in range(N_GENES):
		if randint(0, 1) == 0:
			chromoSon.append(dnaA[i])
		else:
			chromoSon.append(dnaB[i])

	# Applies mutation to the cromosomes generated (the chance of mutation is embedded in the function).
	# Does not apply mutation if one of the parent dnas is the best one (elitism)
	if not elite:
		mutation(chromoSon)

	return chromoSon

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
			offspring.append( Bot( geneticCrossover(parentA.dna, parentB.dna, elite, 'A')    ))
			offspring.append( Bot( geneticCrossover(parentA.dna, parentB.dna, elite, 'B')    ))
		
	elif BREEDING == 'arithmetic':
		# 3x the three possible combinations from arithmetic crossover
		for k in range(3):
			offspring.append( Bot( arithmeticCrossover(parentA.dna, parentB.dna, elite, 'A') ))
			offspring.append( Bot( arithmeticCrossover(parentA.dna, parentB.dna, elite, 'B') ))
			offspring.append( Bot( arithmeticCrossover(parentA.dna, parentB.dna, elite, 'C') ))
		offspring.append( Bot( arithmeticCrossover(parentA.dna, parentB.dna, elite, 'C') ))

	elif BREEDING == 'coinflip':
		# Ten random combinations from coinflip crossover
		for k in range(10):
			offspring.append( Bot( coinflipCrossover(parentA.dna, parentB.dna, elite)    ))

	elif BREEDING == 'mixed':
		# Two possible combinations from genetic crossover
		offspring.append( Bot( geneticCrossover(parentA.dna, parentB.dna, elite, 'A')    ))
		offspring.append( Bot( geneticCrossover(parentA.dna, parentB.dna, elite, 'B')    ))

		# Three possible combinations from arithmetic crossover
		offspring.append( Bot( arithmeticCrossover(parentA.dna, parentB.dna, elite, 'A') ))
		offspring.append( Bot( arithmeticCrossover(parentA.dna, parentB.dna, elite, 'B') ))
		offspring.append( Bot( arithmeticCrossover(parentA.dna, parentB.dna, elite, 'C') ))

		# Five random combinations from coinflip crossover
		for k in range(5):
			offspring.append( Bot( coinflipCrossover(parentA.dna, parentB.dna, elite)    ))

	return offspring

# Gives birth to a whole new generation
def newGen(progenitors):
	newPop = []

	'''
	Every breeding execution generates 10 dnas. Thus, N_BATCH comes to action
	'''

	# This loop breeds all except one pair of parents (i with i+1)
	for i in range(0, N_PROG-1):
		
		# Applying elitism (protection of best dna against mutation)
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
	population = genRandPopulation()

	# Loops for each generation
	for n in range(1, N_GEN+1):
		
		print("----------------------------------------")
		print("Generation", n, ":")

		# Evaluation (population plays the game and their fitness score is set)
		for i in range(0, POP_SIZE):

			training = BotTrain(population[i])
			training.play()

			print("Gen", n,"\tIndiv.", i, "fitness:", population[i].fitness)

		# Selection (individuals are sorted based on their fitness score, the first PROG individuals are selected as progenitors)
		population.sort(key=lambda i:i.fitness, reverse = True)
		progenitors = population[:N_PROG-LUCKY_ONES]

		# Selects a number of lucky ones (random dnas from the population), for the sake of genetic variability
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

		# Best dna of this generations gets the chance to show its abilities
		print("This generation best individual showoff:")
		print("Press ENTER to end...")
		genShowoff = BotGame(progenitors[0], n)
		genShowoff.play()

	input('Training is complete. Press ENTER to watch the best dna play the game.')

	# Visualize the best of the best
	overallShowoff = BotGame(progenitors[0], n)
	overallShowoff.play()
