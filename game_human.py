#!/usr/bin/python3

'''
This is the base version of the Snake game, intended to be played by humans.

The project also contains the machine-destined versions (training and visualization), wich are integrated
to the genetic algorithm.

This version is only a reference to the game algorithm. It has nothing to do with the genetic algorithm and is independent from it.
'''

import sys
from tkinter import *
from time import sleep
from random import randrange

##############################################################################
#                            # CONSTANTS #

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
TIMEOUT = 80
###############################################################################W


class Food(object):

    def __init__(self, canvas):
        self.pos_x = randrange(OFFSET, X_SIZE-OFFSET, PIECE_SIZE)    
        self.pos_y = randrange(OFFSET, Y_SIZE-OFFSET, PIECE_SIZE)
        self.canvas = canvas

    def show(self):
        self.canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+PIECE_SIZE, self.pos_y+PIECE_SIZE, fill="red")

    @property
    def pos(self):
        return self.pos_x, self.pos_y

class Body(object):

    def __init__(self, canvas, head, last_part):
        self.head = head
        self.pos_x = last_part.last_pos_x
        self.pos_y = last_part.last_pos_y
        self.canvas = canvas

        # links the body piece to its previous one, which will be 'followed'
        self.last_part = last_part
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

    def show(self):
        self.canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+PIECE_SIZE, self.pos_y+PIECE_SIZE, fill="black")

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

    def __init__(self, canvas):
        self.pos_x, self.pos_y = START_POS
        self.pos_dir = START_DIR
        self.canvas = canvas
        self.bodySize = 0
        self.last_pos_x = START_POS[0]+PIECE_SIZE
        self.last_pos_y = START_POS[1]

        # reference to the snake's body as a list, starting with one element
        self.body = []
        self.body.append(Body(canvas,self,self))

    def showHead(self):
        self.canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+PIECE_SIZE, self.pos_y+PIECE_SIZE, fill="blue")

    def showBody(self):
        for i in range(0, self.bodySize+1, 1):
            self.body[i].show()

    def show(self):
        self.showHead()
        self.showBody()

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
        if (self.pos_x >= X_SIZE-OFFSET or self.pos_x < OFFSET or self.pos_y >= Y_SIZE-OFFSET or self.pos_y < OFFSET) or (any([parts.pos == self.pos for parts in self.body])):
            return False
        else:
            return True

    def eat(self, food):
        del food
        self.body.append(Body(self.canvas,self,self.body[self.bodySize]))
        self.bodySize += 1

    @property
    def pos(self):
        return self.pos_x, self.pos_y

class Game(object):
    
    def __init__(self, root, canvas, snake, food):
        self.root = root
        self.canvas = canvas
        self.snake = snake
        self.food = food
        self.score = 0
        self.gameState = 1

    def showScore(self):
        self.canvas.create_text(X_SIZE/2, Y_SIZE+OFFSET, text = 'Score: {}'.format(self.snake.bodySize))
        pass

    def keyboardLeft(self, event):
        if (self.snake.InValidPosition()):
            self.snake.turn('LEFT')
    
    def keyboardRight(self, event):
        if (self.snake.InValidPosition()):
            self.snake.turn('RIGHT')
    
    def keyboardUp(self, event):
        if (self.snake.InValidPosition()):
            self.snake.turn('UP')
    
    def keyboardDown(self, event):
        if (self.snake.InValidPosition()):
            self.snake.turn('DOWN')

    def gameOver(self):
        sleep(0.3)
        print('Score: ', self.score )
        self.gameState = 0

    def snakeHasEatenFood(self):
        return self.snake.pos == self.food.pos
            
    def scoreUp(self):
        self.snake.eat(self.food)
        self.food = Food(self.canvas)
        # grants the food will not be in the same pos as the snake
        while ( any([parts.pos == self.food.pos for parts in self.snake.body]) or self.snake.pos == self.food.pos ):
            self.food = Food(canvas)
        self.score += 1

    def showBorder(self):
        self.canvas.create_line(0, OFFSET-4, X_SIZE+4, OFFSET-4, fill="black", width=OFFSET)
        self.canvas.create_line(OFFSET-4, OFFSET-4, OFFSET-4, Y_SIZE, fill="black", width=OFFSET)
        self.canvas.create_line(X_SIZE-4, OFFSET-4, X_SIZE-4, Y_SIZE, fill="black", width=OFFSET)
        self.canvas.create_line(OFFSET-4, Y_SIZE-4, X_SIZE-4, Y_SIZE-4, fill="black", width=OFFSET)

    def tick(self):
        self.canvas.delete("all")

        self.showBorder()
        self.food.show()
        self.snake.show()
        self.showScore()
        
        if not self.snake.InValidPosition():
            self.gameOver()
            return

        if self.snakeHasEatenFood():
            self.scoreUp()

        self.root.update_idletasks()
        self.root.update()
        
        self.snake.walk()
        sleep(TIMEOUT/1000)

if __name__ == '__main__':

    # Tkinter stuff
    root = Tk()
    root.title("Snake")
    canvas = Canvas(root, width=X_SIZE, height=Y_SIZE+SCORE_SIZE)
    canvas.pack(expand = YES, fill = BOTH)

    # Main objects
    snake = SnakeHead(canvas)
    food = Food(canvas)
    game = Game(root, canvas, snake, food)

    # Binding keyboard controls
    root.bind('<Left>', game.keyboardLeft)
    root.bind('<Right>', game.keyboardRight)
    root.bind('<Up>', game.keyboardUp)
    root.bind('<Down>', game.keyboardDown)

    # Main loop    
    while game.gameState:
        game.tick()

    canvas.destroy()
    root.destroy()