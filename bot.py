#!/usr/bin/python3

'''
This is the code related to one individual of the genetic algorithm, from any generation/population.
'''

from random import randint, uniform
import numpy as np
from math import *

class Individual(object):

	def __init__(self, chromosome):
		self.chromosome = chromosome

		self.score = 0
		self.turns = 0
		self.playtime = 0.0
		self.distanceToFood = 0

	def takeAction(self):		

		# Weighs of the controller function (the genes)
		w1   = self.chromosome[0] #  3 		<= 	w1 	<= 99    # expoent of an exponential function
		w2   = self.chromosome[1] #  0.01 	<= 	w2 	<= 1     # multiplicative element of an exponential function

		f1   = self.chromosome[2] #  1   	<= 	f1 	<= 2     # 'a' of an gaussean function
		f2	 = self.chromosome[3] #  0.001 	<= 	f2 	<= 0.003 # 'c' of an gaussean function
		f3   = self.chromosome[4] # -1 		<= 	f3 	<= 1 	 # decision taking constant for choosing wich direction to turn

		# Bot's knowledge of current state of the game
		frontWall = self.data[0] # Normalized distance to wall to the front
		leftWall  = self.data[1] # Normalized distance to wall to the left
		rightWall = self.data[2] # Normalized distance to wall to the right
		foodAngle = self.data[3] # Normalized angle to food

		e = exp(1) # euler number

		##############################################################################
 		# 						# CONTROLLER FUNCTION #

		# Probability of turning this game tick (main controller function)

		wallTurnProb = ((1-frontWall)**w1) *w2
		foodTurnProb = (f1*e)**( -( ((abs(foodAngle)-0.5)**2)/(2*(f2**2)) ) )

		# If the action is taken, probability of what is the side to turn
		leftProb  = leftWall + (f3*foodAngle)
		rightProb = rightWall + (f3*foodAngle)


		# if wallTurnProb > foodTurnProb:
		# 	turnProb = wallTurnProb
		# else:
		# 	turnProb = foodTurnProb

		# turnProb = ( 7*wallTurnProb + 3*foodTurnProb)/10
		turnProb = wallTurnProb
		# turnProb = foodTurnProb
		##############################################################################

		# Taking the action
		rand = uniform(0.0, 1.0)
		if rand <= turnProb:
			self.turns += 1

			if leftProb > rightProb:
				action = -1
			else:
				action = 1
		else:
			action = 0

		return action

	@property
	def fitness(self):
		return self.score
