#!/usr/bin/python3

'''
	this code represents a class derived from BotGame (bot_game.py)

	it is a version of the bot-playable game that does not use graphical interface,
	does not sleep between game ticks and sets game attributes (score, playtime and number of turns)
	back to the bot object when it terminates execution.

	this class is used to evaluate any individual (bot object) from any generation.

	the term 'train' is used instead of 'evaluate'
'''

import game.snake as sn
import game.bot_game as bg
import numpy as np
from math import *
from tweak.ga_tweak import *
from tweak.game_tweak import *
from random import randint, uniform
from time import sleep

# Constant for detecting infinite looping snakes
NOT_score_up_THRESHOLD = 100000

# overwrites some stuff from the main game class, so it is controlled by a bot
class BotTrain(bg.BotGame):

	def __init__(self, bot):
		''' creating 'fake' tkinter objects for ease of implementation.	this way its not needed
		to rewrite everything and some processing is saved because training does not need tkinter
		as it does not uses graphical interface '''
		self.root = None
		self.canvas = None

        # main game objects
		self.snake = sn.Snake(self.canvas)
		self.food  = sn.Food(self.canvas)

		# main game variables
		self.score = 0
		self.playtime = 0.0
		self.turns = 0

		# used to check for infinite looping snakes
		self.last_score_playtime = 0.0
              
		self.is_alive = True

		# reference to the bot thats playing the game
		self.bot = bot

	def tick(self):
		if not self.snake.in_valid_position:
			self.game_over()
			return

		if self.snake_has_eaten_food:
			self.score_up()
			self.last_score_playtime = self.playtime

		''' bot integration related '''
		# bot learns current state of the game and makes a decision
		self.bot.learn_state(self.game_state)
		action = self.bot.take_action()

		# interpreting the action
		self.control_snake(action)
		self.snake.walk()

	def play(self):
		while self.is_alive:
			self.tick()
			self.playtime += 1

			# checks of the ocurrence of an infinite looping snake
			if (self.playtime - self.last_score_playtime) == NOT_score_up_THRESHOLD:
				self.game_over()

		# on game over, set bot's attributes (scores for calculating fitness)
		self.bot.score    = self.score
		self.bot.playtime = self.playtime
		self.bot.turns    = self.turns