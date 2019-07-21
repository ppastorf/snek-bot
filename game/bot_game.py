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

# overwrites some stuff from the main game class, so it is controlled by a bot
class BotGame(sn.Game):
	def __init__(self, bot, gen):
		super().__init__()
		self.root.title("Snek Bot generation " + str(gen))
		self.bot = bot

	@property
	def game_state(self):
		# distance to wall to the front, left and right
		dist_left  = (self.snake.pos_x-OFFSET) / REAL_X_SIZE
		dist_up    = (self.snake.pos_y-OFFSET) / REAL_Y_SIZE
		dist_right = 1-dist_left
		dist_down  = 1-dist_up

		# depending on wich direction the snake is looking, relative walls are different
		if self.snake.direction == 'left':
		    walldist_front  = dist_left
		    walldist_left   = dist_down
		    walldist_right  = dist_up

		if self.snake.direction == 'right':
		    walldist_front  = dist_right
		    walldist_left   = dist_up
		    walldist_right  = dist_down
		    
		if self.snake.direction == 'up':
		    walldist_front  = dist_up
		    walldist_left   = dist_left
		    walldist_right  = dist_right

		if self.snake.direction == 'down':
		    walldist_front  = dist_down
		    walldist_left   = dist_right
		    walldist_right  = dist_left

		# angle to food (normalized)
		foodAngle = degrees( atan2(self.snake.pos_y-self.food.pos_y, self.snake.pos_x-self.food.pos_x)) / 180
		return [walldist_front, walldist_left, walldist_right, foodAngle]

	def control_snake(self, action):
		if action == 'straight':
			pass
		else:
			self.turns += 1
			if self.snake.direction == 'left':
				if action == 'left':
					self.keyboard_down(None)
				if action == 'right':
					self.keyboard_up(None)

			elif self.snake.direction == 'right':
				if action == 'left':
					self.keyboard_up(None)
				if action == 'right':
					self.keyboard_down(None)

			elif self.snake.direction == 'up':
				if action == 'left':
					self.keyboard_left(None)
				if action == 'right':
					self.keyboard_right(None)

			elif self.snake.direction == 'down':
				if action == 'left':
					self.keyboard_right(None)
				if action == 'right':
					self.keyboard_left(None)

	def _end_game(self, event):
		self.game_over()

	def _tick(self):
       	# clear screen
		self.canvas.delete("all")

		self.show_border()
		self.food.show()
		self.snake.show()
		self.show_score()

		if not self.snake.in_valid_position:
			self.game_over()
			return

		if self.snake_has_eaten_food:
		    self.score_up()

		# bot learns current state of the game and makes a decision
		self.bot.learn_state(self.game_state)
		action = self.bot.take_action()

		# interpreting the action
		self.control_snake(action)

		# draw screen
		self.root.update_idletasks()
		self.root.update()

		self.snake.walk()


	def play(self):
		# binding to end demonstration
		self.root.bind('<Return>', self._end_game)

		# main loop
		while self.is_alive:
			self._tick()
			sleep(BOT_SHOW_TIMEOUT)

		# on game over
		sleep(0.3)
		self.end()