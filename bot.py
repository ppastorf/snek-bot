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

	def __init__(self, dna):
		''' 
		bot's DNA: contains all information that defines a bot individual
		it is the values wich the bot will use to calculate it action
		based on it's current information about the game state '''
		self.dna = dna

		# bot's current information about the game state
		self.data = []

		# used to set this individual's fitness
		self.score = 0
		self.turns = 0
		self.playtime = 0.0
		self.distance_to_food = 0

	@property
	def fitness(self):
		return self.score

	def learn_state(self, data):
		self.data = data

	'''
	take some action based on the bot's current knowledge of the game state.
	returns either 'straight' (no action), 'left' or 'right' '''
	def take_action(self):	
		# Weighs of the controller function (the genes)
		w1   = self.dna[0] #  3 		<= 	w1 	<= 99    # expoent of an exponential function
		w2   = self.dna[1] #  0.01 	<= 	w2 	<= 1     # multiplicative element of an exponential function

		f1   = self.dna[2] #  1   	<= 	f1 	<= 2     # 'a' of an gaussean function
		f2	 = self.dna[3] #  0.001 	<= 	f2 	<= 0.003 # 'c' of an gaussean function
		f3   = self.dna[4] # -1 		<= 	f3 	<= 1 	 # decision taking constant for choosing wich direction to turn

		# Bot's knowledge of current state of the game
		front_wall = self.data[0] # Normalized distance to wall to the front
		left_watt  = self.data[1] # Normalized distance to wall to the left
		right_wall = self.data[2] # Normalized distance to wall to the right
		food_angle = self.data[3] # Normalized angle to food

		e = exp(1) # euler number

		##############################################################################
 		# 						# CONTROLLER FUNCTION #

		# Probability of turning this game tick (main controller function)

		turn_prob_wall = ((1-front_wall)**w1) *w2
		turn_prob_food = (f1*e)**( -( ((abs(food_angle)-0.5)**2)/(2*(f2**2)) ) )

		# If the action is taken, probability of what is the side to turn
		left_turn_prob  = left_watt  + (f3*food_angle)
		right_turn_prob = right_wall + (f3*food_angle)

		turn_prob = turn_prob_wall *0.7 + turn_prob_food*0.3
		##############################################################################

		# Taking the action
		rand = uniform(0.0, 1.0)
		if rand <= turn_prob:

			if left_turn_prob > right_turn_prob:
				action = 'left'
			else:
				action = 'right'
		else:
			action = 'straight'

		return action