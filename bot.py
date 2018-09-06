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
		w1   = self.chromosome[0] # 3.00 <=  w1   <= 99.0
		w2   = self.chromosome[1] # 0.01 <=  w2   <= 2.00

		f1   = self.chromosome[2] # 3.00 <=  f1   <= 99.0
		f2   = self.chromosome[3] # -1.0 <=  f3   <= 1.00
		
		fxw1 = self.chromosome[4] # 0.01 <=  fxw1 <= 1.00

		frontWall = self.data[0] # Normalized distance to wall to the front
		leftWall  = self.data[1] # Normalized distance to wall to the left
		rightWall = self.data[2] # Normalized distance to wall to the right
		foodAngle = self.data[3] # Normalized angle to food


		##############################################################################
 		# 						# CONTROLLER FUNCTION #

		# Probability of turning this game tick (main controller function)

		turnProb = (  (( ((1-frontWall)**w1) * w2) * ( (abs(foodAngle)*f1) ))  - ( ((1-frontWall)*foodAngle) *fxw1 ) )

		# If the action is taken, probability of what is the side to turn
		leftProb  = leftWall + (f2*foodAngle)
		rightProb = rightWall + (f2*foodAngle)

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
