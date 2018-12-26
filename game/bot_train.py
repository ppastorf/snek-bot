#!/usr/bin/python3

'''
	this code represents a class derived from BotGame (bot_game.py)

	it is a version of the bot-playable game that does not use graphical interface,
	does not sleep between game ticks and sets game attributes (score, playtime and number of turns)
	back to the bot object when it terminates execution.

	basically, this class is used to evaluate any individual (bot object) from any generation.

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
NOT_SCOREUP_THRESHOLD = 100000

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
		self.lastScoreUpPlaytime = 0.0
              
		self.isAlive = True

		# reference to the bot thats playing the game
		self.bot = bot

	def tick(self):

		if not self.snake.inValidPosition:
			self.gameOver()
			return

		if self.snakeHasEatenFood:
			self.scoreUp()
			
			'''
			everytime the snake gets a score up, saves the current
			playtime. this is used to check for infinite
			looping snakes.
			'''
			self.lastScoreUpPlaytime = self.playtime


		''' bot integration related '''
		# bot learns current state of the game
		self.bot.learnState(self.gameState)

		# bot decides what to do
		action = self.bot.takeAction()

		# interpreting the action
		self.controlSnake(action)
		''''''

		self.snake.walk()

	def play(self):

		# main loop
		while self.isAlive:

			# ticks the game
			self.tick()
			self.playtime += 1

			# checks of the ocurrence of an infinite looping snake
			if (self.playtime - self.lastScoreUpPlaytime) == NOT_SCOREUP_THRESHOLD:
				self.gameOver()


		# on game over, set bot's attributes (scores for calculating fitness)
		self.bot.setScore(self.score)
		self.bot.setPlaytime(self.playtime)
		self.bot.setTurns(self.turns)