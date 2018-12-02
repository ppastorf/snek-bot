#!/usr/bin/python3

'''
This is the machine version of the Snake game, intended to be played by any specific individual from any generation of the genetic algorithm.

This version is intended to be the way to visualize the actal performance of an chromosome.
The chromosome is passed as argument to the play() functions, wich is the main procedure of the algorithm.
'''

import sys
from tkinter import *
from time import sleep
from random import randrange, uniform
import numpy as np
from math import *

from bot import *
from tweak.game_tweak import *
from tweak.ga_tweak import *

# Numpy stuff for printing arrays
np.set_printoptions(threshold=np.nan)




    def prepBotInfo(self):
        
        # distance to wall to the front, left and right
        distLeft  = (self.snake.pos_x-OFFSET) / REAL_X_SIZE
        distUp    = (self.snake.pos_y-OFFSET) / REAL_Y_SIZE
        distRight = 1-distLeft
        distDown  = 1-distUp

        # depending on wich direction the snake is looking, relative walls are different
        if self.snake.pos_dir == 'left':
            wallDistFront  = distLeft
            wallDistLeft   = distDown
            walllDistRight = distUp

        if self.snake.pos_dir == 'RIGHT':
            wallDistFront  = distRight
            wallDistLeft   = distUp
            walllDistRight = distDown
            
        if self.snake.pos_dir == 'u':
            wallDistFront  = distUp
            wallDistLeft   = distLeft
            walllDistRight = distRight
        
        if self.snake.pos_dir == 'down':
            wallDistFront  = distDown
            wallDistLeft   = distRight
            walllDistRight = distLeft

        # angle to food (normalized)
        foodAngle = degrees( atan2(self.snake.pos_y-self.food.pos_y, self.snake.pos_x-self.food.pos_x)) / 180
        return [wallDistFront, wallDistLeft, walllDistRight, foodAngle]

    def botAction(self, action):
        if action == 0:
            pass

        if action == -1:
            if self.snake.pos_dir ==  'left':
                self.snake.turn('down')
                return
            if self.snake.pos_dir ==  'down':
                self.snake.turn('RIGHT')
                return
            if self.snake.pos_dir ==  'RIGHT':
                self.snake.turn('u')
                return
            if self.snake.pos_dir ==  'u':
                self.snake.turn('left')
                return

        if action == 1:
            if self.snake.pos_dir ==  'RIGHT':
                self.snake.turn('down')
                return
            if self.snake.pos_dir ==  'down':
                self.snake.turn('left')
                return
            if self.snake.pos_dir ==  'left':
                self.snake.turn('u')
                return
            if self.snake.pos_dir ==  'u':
                self.snake.turn('RIGHT')
                return

        ############ BOT INTERACTION #############
        # bot gets the information input about the current game state
        self.bot.data = self.prepBotInfo()

        # bot takes an action based on its information;
        action = self.bot.takeAction()

        # interpreting bot's action into the game
        self.botAction(action)
        #########################################

        self.snake.walk()

        self.bot.playtime += TIMEOUT
