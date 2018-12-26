#!/usr/bin/python3

'''
	this code represents a version of the game to be played by a bot, with graphical interface (tkinter stuff)

	this class intended to be used to show a bot's performance after being trained
'''

import game.snake as sn
import numpy as np
from math import *
from tweak.ga_tweak import *
from tweak.game_tweak import *
from random import randint, uniform
from time import sleep

# Numpy stuff for printing arrays
np.set_printoptions(threshold=np.nan)

# overwrites some stuff from the main game class, so it is controlled by a bot
class BotGame(sn.Game):
	def __init__(self, bot, gen):
		super().__init__()
		self.root.title("Snek Bot generation " + str(gen))

		# reference to the bot thats playing the game
		self.bot = bot

	@property
	def gameState(self):
		# distance to wall to the front, left and right
		distLeft  = (self.snake.pos_x-OFFSET) / REAL_X_SIZE
		distUp    = (self.snake.pos_y-OFFSET) / REAL_Y_SIZE
		distRight = 1-distLeft
		distDown  = 1-distUp

		# depending on wich direction the snake is looking, relative walls are different
		if self.snake.direction == 'left':
		    wallDistFront  = distLeft
		    wallDistLeft   = distDown
		    wallDistRight = distUp

		if self.snake.direction == 'right':
		    wallDistFront  = distRight
		    wallDistLeft   = distUp
		    wallDistRight = distDown
		    
		if self.snake.direction == 'up':
		    wallDistFront  = distUp
		    wallDistLeft   = distLeft
		    wallDistRight = distRight

		if self.snake.direction == 'down':
		    wallDistFront  = distDown
		    wallDistLeft   = distRight
		    wallDistRight = distLeft

		# angle to food (normalized)
		foodAngle = degrees( atan2(self.snake.pos_y-self.food.pos_y, self.snake.pos_x-self.food.pos_x)) / 180
		return [wallDistFront, wallDistLeft, wallDistRight, foodAngle]

	def controlSnake(self, action):
		if action == 'straight':
			pass
		else:
			self.turns += 1
			if self.snake.direction == 'left':
				if action == 'left':
					self.keyboardDown(None)
				if action == 'right':
					self.keyboardUp(None)

			elif self.snake.direction == 'right':
				if action == 'left':
					self.keyboardUp(None)
				if action == 'right':
					self.keyboardDown(None)

			elif self.snake.direction == 'up':
				if action == 'left':
					self.keyboardLeft(None)
				if action == 'right':
					self.keyboardRight(None)

			elif self.snake.direction == 'down':
				if action == 'left':
					self.keyboardRight(None)
				if action == 'right':
					self.keyboardLeft(None)

	def endGame(self, event):
		self.gameOver()

	def tick(self):

       # clear screen
		self.canvas.delete("all")

		self.showBorder()
		self.food.show()
		self.snake.show()
		self.showScore()

		if not self.snake.inValidPosition:
			self.gameOver()
			return

		if self.snakeHasEatenFood:
		    self.scoreUp()

		''''''
		# bot learns current state of the game
		self.bot.learnState(self.gameState)

		# bot decides what to do
		action = self.bot.takeAction()

		# interpreting the action
		self.controlSnake(action)
		''''''

		# draw screen
		self.root.update_idletasks()
		self.root.update()

		self.snake.walk()


	def play(self):

		# binding to end demonstration
		self.root.bind('<Return>', self.endGame)

		# main loop
		while self.isAlive:
			self.tick()
			sleep(BOT_SHOW_TIMEOUT)

		# on game over
		sleep(0.3)
		self.end()