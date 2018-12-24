#!/usr/bin/python3

'''
    contains all classes for the base snake game
'''

import sys
from tkinter import *
from random import randrange
from tweak.game_tweak import *
from time import sleep

class Element(object):
    def __init__(self, canvas, pos_x, pos_y, color):
        self.canvas = canvas
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y

    def show(self):
        self.canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+PIECE_SIZE, self.pos_y+PIECE_SIZE, fill=self.color)

    @property
    def pos(self):
        return self.pos_x, self.pos_y

class Food(Element):

    def __init__(self, canvas):
        super().__init__(canvas, randrange(OFFSET, X_SIZE-OFFSET, PIECE_SIZE), randrange(OFFSET, Y_SIZE-OFFSET, PIECE_SIZE), FOOD_COLOR)

class SnakeBody(Element):

    def __init__(self, canvas, lastPart):

        super().__init__(canvas, lastPart.lastPos_x, lastPart.lastPos_y, BODY_COLOR)

        # links the body piece to its previous one, which will be 'followed'
        self.lastPart = lastPart
        self.lastPos_x = self.pos_x
        self.lastPos_y = self.pos_y

    def walk(self):
        # updates its last position to its current one
        self.lastPos_x = self.pos_x
        self.lastPos_y = self.pos_y

        # updates itself's position to the previous part's last position
        self.pos_x = self.lastPart.lastPos_x
        self.pos_y = self.lastPart.lastPos_y

class SnakeHead(Element):

    def __init__(self, canvas):
        super().__init__(canvas, START_POS[0], START_POS[1], HEAD_COLOR)
        self.lastPos_x = START_POS[0]+PIECE_SIZE
        self.lastPos_y = START_POS[1]

    def walk(self, direction):
        # saves the last position of the head
        self.lastPos_x = self.pos_x
        self.lastPos_y = self.pos_y
        
        # walks
        if direction == 'left':
            self.pos_x -= PIECE_SIZE

        if direction == 'right':
            self.pos_x += PIECE_SIZE

        if direction == 'up':
            self.pos_y -= PIECE_SIZE

        if direction == 'down':
            self.pos_y += PIECE_SIZE

class Snake(object):

    def __init__(self, canvas):

        # the snake has a direction, head, body and reference to the canvas to be shown 
        self.direction = START_DIR
        self.canvas = canvas

        # head element
        self.head = SnakeHead(canvas)

        # reference to the snake's body as a list, starting with one element
        self.body = []
        self.body.append(SnakeBody(canvas, self.head))

    def showBody(self):
        for i in range(0, self.bodySize, 1):
            self.body[i].show()

    def show(self):
        self.head.show()
        self.showBody()

    def walk(self):

        # walks the head
        self.head.walk(self.direction)

        # walks the rest of the body
        for i in range(0, self.bodySize, 1):
           self.body[i].walk()

    def turn(self, newDir):
        if newDir == 'left':
            if self.direction != 'right':
                self.direction = 'left'

        if newDir == 'right':
            if self.direction != 'left':
                self.direction = 'right'

        if newDir == 'up':
            if self.direction != 'down':
                self.direction = 'up'

        if newDir == 'down':
            if self.direction != 'up':
                self.direction = 'down'

    @property
    def pos_x(self):                
        return self.head.pos_x

    @property
    def pos_y(self):                
        return self.head.pos_y

    @property
    def pos(self):                
        return self.head.pos

    @property
    def bodySize(self):
        return len(self.body)

    @property
    def inValidPosition(self):
        return not (
            ( self.pos_x >= X_SIZE-OFFSET or self.pos_x < OFFSET
            or
            self.pos_y >= Y_SIZE-OFFSET or self.pos_y < OFFSET ) 
            or
            ( any([parts.pos == self.pos for parts in self.body]) )
            )

    def eat(self, food):
        del food
        self.body.append(SnakeBody(self.canvas, self.body[self.bodySize-1]))

class Game(object):
    
    def __init__(self):
        # creating tkinter objects
        self.root = Tk()
        self.root.title("Snake")
        self.canvas = Canvas(self.root, width=X_SIZE, height=Y_SIZE+SCORE_SIZE)
        self.canvas.pack(expand = YES, fill = BOTH)

        # main game objects
        self.snake = Snake(self.canvas)
        self.food  = Food(self.canvas)

        # main game variables
        self.score = 0
        self.playtime = 0.0
        self.turns = 0

        self.isAlive = True

    def showScore(self):
        self.canvas.create_text(X_SIZE/2, Y_SIZE+OFFSET, text='Score: {}'.format(self.score))

    def keyboardLeft(self, event):
        if self.snake.inValidPosition:
            self.turns += 1
            self.snake.turn('left')
    
    def keyboardRight(self, event):
        if self.snake.inValidPosition:
            self.turns += 1
            self.snake.turn('right')
    
    def keyboardUp(self, event):
        if self.snake.inValidPosition:
            self.turns += 1
            self.snake.turn('up')
    
    def keyboardDown(self, event):
        if self.snake.inValidPosition:
            self.turns += 1
            self.snake.turn('down')

    def gameOver(self):
        self.isAlive = False

    @property
    def snakeHasEatenFood(self):
        return self.snake.pos == self.food.pos
            
    def scoreUp(self):
        self.snake.eat(self.food)
        self.food = Food(self.canvas)
        # grants the food will not be in the same pos as the snake
        while ( any([parts.pos == self.food.pos for parts in self.snake.body]) or self.snake.pos == self.food.pos ):
            self.food = Food(self.canvas)
        self.score += 1

    def showBorder(self):
        self.canvas.create_line(0, OFFSET-4, X_SIZE+4, OFFSET-4, fill=BORD_COLOR, width=OFFSET)
        self.canvas.create_line(OFFSET-4, OFFSET-4, OFFSET-4, Y_SIZE, fill=BORD_COLOR, width=OFFSET)
        self.canvas.create_line(X_SIZE-4, OFFSET-4, X_SIZE-4, Y_SIZE, fill=BORD_COLOR, width=OFFSET)
        self.canvas.create_line(OFFSET-4, Y_SIZE-4, X_SIZE-4, Y_SIZE-4, fill=BORD_COLOR, width=OFFSET)

    def tick(self):

        # clear sceen
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

        # draw screen
        self.root.update_idletasks()
        self.root.update()
        
        self.snake.walk()

    def end(self):
        # terminates tkinter objects
        self.canvas.destroy()
        self.root.destroy()

    def play(self):

        # main loop
        while self.isAlive:
            self.tick()
            self.playtime += HUMAN_TIMEOUT
            sleep(HUMAN_TIMEOUT)

        # on game over
        sleep(0.3)
        print('Score: ', self.score)
        self.end()