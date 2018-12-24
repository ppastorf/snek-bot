#!/usr/bin/python3

from random import randint, uniform
import numpy as np
from math import *
from tweak.ga_tweak import *
from tweak.game_tweak import *

'''
	code related to a bot: an individual of the genetic algorithm
'''

class Bot(object):

	def __init__(self, genome):
		''' 
		bot's DNA: contains all information that defines a bot individual
		it is the values wich the bot will use to calculate it action
		based on it's current information about the game state '''
		self.genome = genome

		# bot's current information about the game state
		self.data = []

		# used to set this individual's fitness
		self.score = 0
		self.turns = 0
		self.playtime = 0.0
		self.distanceToFood = 0

	@property
	def fitness(self):
		return self.score

	def setScore(self, value):
		self.score = value

	def setPlaytime(self, value):
		self.playtime = value

	def setTurns(self, value):
		self.turns = value

	def learnState(self, data):
		self.data = data

	'''
	take some action based on the bot's current knowledge of the game state.
	returns either 'straight' (no action), 'left' or 'right' '''
	def takeAction(self):	

		# Weighs of the controller function (the genes)
		w1   = self.genome[0] #  3 		<= 	w1 	<= 99    # expoent of an exponential function
		w2   = self.genome[1] #  0.01 	<= 	w2 	<= 1     # multiplicative element of an exponential function

		f1   = self.genome[2] #  1   	<= 	f1 	<= 2     # 'a' of an gaussean function
		f2	 = self.genome[3] #  0.001 	<= 	f2 	<= 0.003 # 'c' of an gaussean function
		f3   = self.genome[4] # -1 		<= 	f3 	<= 1 	 # decision taking constant for choosing wich direction to turn

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

			if leftProb > rightProb:
				action = 'left'
			else:
				action = 'right'
		else:
			action = 'straight'

		return action