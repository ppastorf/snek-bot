#!/usr/bin/python3

'''
This is the base version of the Snake game, intended to be played by humans.

The project also contains the machine-destined version, wich will be integrated
to the genetic algorithm...
'''

import sys
from tkinter import *
from time import sleep
from random import randrange

# Constants class
class Cons():
   
    X_SIZE = 400
    Y_SIZE = 400
    PIECE_SIZE = 10
    SCORE_SIZE = 20
    OFFSET = PIECE_SIZE
    START_POS = [300,200]
    START_DIR = 'LEFT'
    TIMEOUT = 80

class Food(object):

    def __init__(self, canvas):
        self.pos_x = randrange(Cons.OFFSET, Cons.X_SIZE-Cons.OFFSET, Cons.PIECE_SIZE)    
        self.pos_y = randrange(Cons.OFFSET, Cons.Y_SIZE-Cons.OFFSET, Cons.PIECE_SIZE)
        self.canvas = canvas

    def show(self):
        self.canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+Cons.PIECE_SIZE, self.pos_y+Cons.PIECE_SIZE, fill="red")

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
        self.canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+Cons.PIECE_SIZE, self.pos_y+Cons.PIECE_SIZE, fill="black")

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
        self.pos_x, self.pos_y = Cons.START_POS
        self.pos_dir = Cons.START_DIR
        self.canvas = canvas
        self.bodySize = 0
        self.last_pos_x = Cons.START_POS[0]+Cons.PIECE_SIZE
        self.last_pos_y = Cons.START_POS[1]

        # reference to the snake's body as a list, starting with one element
        self.body = []
        self.body.append(Body(canvas,self,self))

    def showHead(self):
        self.canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+Cons.PIECE_SIZE, self.pos_y+Cons.PIECE_SIZE, fill="blue")

    def showBody(self):
        for i in range(0, snake.bodySize+1, 1):
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
            self.pos_x -= Cons.PIECE_SIZE

        if self.pos_dir == 'RIGHT':
            self.pos_x += Cons.PIECE_SIZE

        if self.pos_dir == 'UP':
            self.pos_y -= Cons.PIECE_SIZE

        if self.pos_dir == 'DOWN':
            self.pos_y += Cons.PIECE_SIZE

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
        if (self.pos_x >= Cons.X_SIZE-Cons.OFFSET or self.pos_x < Cons.OFFSET or self.pos_y >= Cons.Y_SIZE-Cons.OFFSET or self.pos_y < Cons.OFFSET) or (any([parts.pos == self.pos for parts in self.body])):
            return False
        else:
            return True

    def eat(self, food):
        del food
        self.body.append(Body(canvas,self,self.body[self.bodySize]))
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

    def showScore(self):
        self.canvas.create_text(Cons.X_SIZE/2, Cons.Y_SIZE+Cons.OFFSET, text = 'Score: {}'.format(snake.bodySize))
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
        sys.exit(0)

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
        self.canvas.create_line(0, Cons.OFFSET-4, Cons.X_SIZE+4, Cons.OFFSET-4, fill="black", width=Cons.OFFSET)
        self.canvas.create_line(Cons.OFFSET-4, Cons.OFFSET-4, Cons.OFFSET-4, Cons.Y_SIZE, fill="black", width=Cons.OFFSET)
        self.canvas.create_line(Cons.X_SIZE-4, Cons.OFFSET-4, Cons.X_SIZE-4, Cons.Y_SIZE, fill="black", width=Cons.OFFSET)
        self.canvas.create_line(Cons.OFFSET-4, Cons.Y_SIZE-4, Cons.X_SIZE-4, Cons.Y_SIZE-4, fill="black", width=Cons.OFFSET)

    def tick(self):
        self.canvas.delete("all")

        self.showBorder()
        self.food.show()
        self.snake.show()
        self.showScore()
        
        if not self.snake.InValidPosition():
            self.gameOver()

        if self.snakeHasEatenFood():
            self.scoreUp()

        self.root.update_idletasks()
        self.root.update()
        
        snake.walk()
        sleep(Cons.TIMEOUT/1000)

if __name__ == '__main__':
        
    # Tkinter stuff
    root = Tk()
    root.title("Snake")
    canvas = Canvas(root, width=Cons.X_SIZE, height=Cons.Y_SIZE+Cons.SCORE_SIZE)
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
    while True:
        game.tick()