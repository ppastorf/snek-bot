#!/usr/bin/python3

'''
This is the training version of the game. There's no timeout between gam ticks and no interface at all.
This version of the game is intended only to test individuals from any generation of population and its part of the genetic algorithm.

The Evaluate() function is the main procedure and receives an bot individual as argument.
The bot plays the game and its playing statistics (score, playtime, etc) are stored directly into the individual object that 'played' the game.

This version of the game is only to be accessed by the main genetic algorithm execution.
'''

import bot
import sys
from time import sleep
from random import randrange, uniform
import numpy as np
from math import *

# CONSTANTS ############################

# Total size of the game screen
X_SIZE = 400
Y_SIZE = 400

# Size of the score display on the bottom of the screen
SCORE_SIZE = 20

# Size of a piece (block wich constitutes every part of the snake, the food and the offset borders)
PIECE_SIZE = 10

# Size of the offset border
OFFSET = PIECE_SIZE

# Size of the playable portion of the screen (game screen - offset borders)
REAL_X_SIZE = X_SIZE-OFFSET
REAL_Y_SIZE = Y_SIZE-OFFSET

# Starting values of the snake's head
START_POS = [300,200]
START_DIR = 'LEFT'

# Timeout between every game tick (in miliseconds) 
TIMEOUT = 1

######################################

class Food(object):

    def __init__(self):
        self.pos_x = randrange(OFFSET, REAL_X_SIZE, PIECE_SIZE)  
        self.pos_y = randrange(OFFSET, REAL_Y_SIZE, PIECE_SIZE)

    @property
    def pos(self):
        return self.pos_x, self.pos_y

class Body(object):

    def __init__(self, head, last_part):
        self.head = head
        self.pos_x = last_part.last_pos_x
        self.pos_y = last_part.last_pos_y

        # links the body piece to its previous one, which will be 'followed'
        self.last_part = last_part
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

    def walk(self):
        # updates its last position to its current one
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

        # updates itself's position to the previous part's last position
        self.pos_x = self.last_part.last_pos_x
        self.pos_y = self.last_part.last_pos_y

    @property
    def pos(self):
        return self.pos_x, self.pos_y

class SnakeHead(object):

    def __init__(self):
        self.pos_x, self.pos_y = START_POS
        self.pos_dir = START_DIR
        self.bodySize = 0
        self.last_pos_x = START_POS[0]+PIECE_SIZE
        self.last_pos_y = START_POS[1]

        # reference to the snake's body as a list, starting with one element
        self.body = []
        self.body.append(Body(self,self))

    def walk(self):
        # Saves the last position of the head
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y
        
        # Walks the head itself
        if self.pos_dir == 'LEFT':
            self.pos_x -= PIECE_SIZE

        if self.pos_dir == 'RIGHT':
            self.pos_x += PIECE_SIZE

        if self.pos_dir == 'UP':
            self.pos_y -= PIECE_SIZE

        if self.pos_dir == 'DOWN':
            self.pos_y += PIECE_SIZE

        # Walks the rest of the body
        for i in range(0, self.bodySize+1, 1):
           self.body[i].walk()

    def turn(self, new_dir):
        if new_dir == 'LEFT':
            if self.pos_dir != 'RIGHT':
                self.pos_dir = 'LEFT'

        if new_dir == 'RIGHT':
            if self.pos_dir != 'LEFT':
                self.pos_dir = 'RIGHT'

        if new_dir == 'UP':
            if self.pos_dir != 'DOWN':
                self.pos_dir = 'UP'

        if new_dir == 'DOWN':
            if self.pos_dir != 'UP':
                self.pos_dir = 'DOWN'

    def InValidPosition(self):
        if (self.pos_x >= REAL_X_SIZE or self.pos_x < OFFSET or self.pos_y >= REAL_Y_SIZE or self.pos_y < OFFSET) or (any([parts.pos == self.pos for parts in self.body])):
            return False
        else:
            return True

    def eat(self, food):
        del food
        self.body.append(Body(self,self.body[self.bodySize]))
        self.bodySize += 1

    @property
    def pos(self):
        return self.pos_x, self.pos_y

class Evalutator(object):
    
    def __init__(self, snake, food, bot):
        self.snake = snake
        self.food = food
        self.score = 0
        self.bot = bot
        self.gameState = 1

    def gameOver(self):
        # sleep(0.3)
        self.gameState = 0

    def snakeHasEatenFood(self):
        return self.snake.pos == self.food.pos
            
    def scoreUp(self):
        self.snake.eat(self.food)
        self.food = Food()
        # grants the food will not be in the same pos as the snake
        while ( any([parts.pos == self.food.pos for parts in self.snake.body]) or self.snake.pos == self.food.pos ):
            self.food = Food()
        self.bot.score += 1
        self.score += 1

    def prepBotInfo(self):
        
        # Distance to wall to the front, left and right
        # As the neural network inputs have to be between -1 and 1, dividing by the sizes normalizes the values
        distLeft  = (self.snake.pos_x-OFFSET) / REAL_X_SIZE
        distUp    = (self.snake.pos_y-OFFSET) / REAL_Y_SIZE
        distRight = 1-distLeft
        distDown  = 1-distUp

        # Depending on wich direction the snake is looking, relative walls are different
        if self.snake.pos_dir == 'LEFT':
            wallDistFront  = distLeft
            wallDistLeft   = distDown
            walllDistRight = distUp

        if self.snake.pos_dir == 'RIGHT':
            wallDistFront  = distRight
            wallDistLeft   = distUp
            walllDistRight = distDown
            
        if self.snake.pos_dir == 'UP':
            wallDistFront  = distUp
            wallDistLeft   = distLeft
            walllDistRight = distRight
        
        if self.snake.pos_dir == 'DOWN':
            wallDistFront  = distDown
            wallDistLeft   = distRight
            walllDistRight = distLeft

        # Angle to food (normalized)
        foodAngle = degrees(atan2(self.snake.pos_y-self.food.pos_y, self.snake.pos_x-self.food.pos_x)) / 180

        return [wallDistFront, wallDistLeft, walllDistRight, foodAngle]

    def botAction(self, action):
        if action == 0:
            pass

        if action == -1:
            if self.snake.pos_dir ==  'LEFT':
                self.snake.turn('DOWN')
                return
            if self.snake.pos_dir ==  'DOWN':
                self.snake.turn('RIGHT')
                return
            if self.snake.pos_dir ==  'RIGHT':
                self.snake.turn('UP')
                return
            if self.snake.pos_dir ==  'UP':
                self.snake.turn('LEFT')
                return

        if action == 1:
            if self.snake.pos_dir ==  'RIGHT':
                self.snake.turn('DOWN')
                return
            if self.snake.pos_dir ==  'DOWN':
                self.snake.turn('LEFT')
                return
            if self.snake.pos_dir ==  'LEFT':
                self.snake.turn('UP')
                return
            if self.snake.pos_dir ==  'UP':
                self.snake.turn('RIGHT')
                return

    def tick(self):

        if not self.snake.InValidPosition():
            self.gameOver()
            return

        if self.snakeHasEatenFood():
            self.scoreUp()

        ############ BOT INTERACTION #############
        # Bot gets the information input about the current game state
        self.bot.data = self.prepBotInfo()

        # Bot's neural network takes a decision based on its information
        action = self.bot.takeAction()

        # Interpreting bot's action into the game
        self.botAction(action)
        #########################################

        self.snake.walk()

        self.bot.playtime += TIMEOUT/1000

        # Case the snake is in a infinite loop
        if self.bot.playtime >= 100:
            self.gameOver()
            return
            
def Evaluate(individual):

    # Bot object (individual)
    bot = individual

    # Main objects
    snake = SnakeHead()
    food = Food()
    game = Evalutator(snake, food, bot)

    # Main loop
    while game.gameState:
        game.tick()