from tkinter import *
from random import randrange
from tweak.game_tweak import *
from time import sleep

# Total size of the game screen
X_SIZE = 400
Y_SIZE = 400

# Size of the playable portion of the screen (game screen - offset borders)
OFFSET = 10

REAL_X_SIZE = X_SIZE - OFFSET
REAL_Y_SIZE = Y_SIZE - OFFSET

SCORE_SIZE = 20
PIECE_SIZE = 10

# Starting values of the snake's head
START_POS = [300, 200]
START_DIR = 'left'

# Timeout between every game tick in seconds
HUMAN_TIMEOUT = 0.040
BOT_SHOW_TIMEOUT = 0.010

# Elements color
FOOD_COLOR = "#006600"
HEAD_COLOR = "#804d00"
BODY_COLOR = "#e68a00"
BORD_COLOR = "#000000"


class Element(object):
    def __init__(self, canvas, pos_x, pos_y, color):
        self.canvas = canvas
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y

    def show(self):
        self.canvas.create_rectangle(self.pos_x,
                                     self.pos_y,
                                     self.pos_x + PIECE_SIZE,
                                     self.pos_y + PIECE_SIZE,
                                     fill=self.color)

    @property
    def pos(self):
        return self.pos_x, self.pos_y


class Food(Element):
    def __init__(self, canvas):
        super().__init__(canvas,
                         randrange(OFFSET, X_SIZE - OFFSET, PIECE_SIZE),
                         randrange(OFFSET, Y_SIZE - OFFSET, PIECE_SIZE),
                         FOOD_COLOR)


class SnakeBody(Element):

    def __init__(self, canvas, last_part):
        super().__init__(canvas,
                         last_part.last_pos_x,
                         last_part.last_pos_y,
                         BODY_COLOR)

        # links the body piece to its previous one
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


class SnakeHead(Element):

    def __init__(self, canvas):
        super().__init__(canvas,
                         START_POS[0],
                         START_POS[1],
                         HEAD_COLOR)

        self.last_pos_x = START_POS[0] + PIECE_SIZE
        self.last_pos_y = START_POS[1]

    def walk(self, direction):
        # saves the last position of the head
        self.last_pos_x = self.pos_x
        self.last_pos_y = self.pos_y

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
        self.direction = START_DIR
        self.canvas = canvas

        self.head = SnakeHead(canvas)
        self.body = [SnakeBody(canvas, self.head)]

    def show_body(self):
        for i in range(0, self.body_size, 1):
            self.body[i].show()

    def show(self):
        self.head.show()
        self.show_body()

    def walk(self):
        self.head.walk(self.direction)

        for i in range(0, self.body_size, 1):
            self.body[i].walk()

    def turn(self, new_dir):
        if new_dir == 'left':
            if self.direction != 'right':
                self.direction = 'left'

        if new_dir == 'right':
            if self.direction != 'left':
                self.direction = 'right'

        if new_dir == 'up':
            if self.direction != 'down':
                self.direction = 'up'

        if new_dir == 'down':
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
    def body_size(self):
        return len(self.body)

    @property
    def in_valid_position(self):
        return not (
            (self.pos_x >= X_SIZE - OFFSET or self.pos_x < OFFSET or
             self.pos_y >= Y_SIZE - OFFSET or self.pos_y < OFFSET) or
            (any([parts.pos == self.pos for parts in self.body]))
        )

    def eat(self, food):
        del food
        self.body.append(SnakeBody(self.canvas, self.body[self.body_size - 1]))


class Game(object):

    def __init__(self):
        self.root = Tk()
        self.root.title("Snake")
        self.canvas = Canvas(self.root, width=X_SIZE,
                             height=Y_SIZE + SCORE_SIZE)
        self.canvas.pack(expand=YES, fill=BOTH)

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

        self.score = 0
        self.playtime = 0.0
        self.turns = 0

        self.is_alive = True

    def show_score(self):
        self.canvas.create_text(
            X_SIZE / 2,
            Y_SIZE + OFFSET,
            text='Score: {}'.format(self.score))

    def keyboard_left(self, event):
        if self.snake.in_valid_position:
            self.turns += 1
            self.snake.turn('left')

    def keyboard_right(self, event):
        if self.snake.in_valid_position:
            self.turns += 1
            self.snake.turn('right')

    def keyboard_up(self, event):
        if self.snake.in_valid_position:
            self.turns += 1
            self.snake.turn('up')

    def keyboard_down(self, event):
        if self.snake.in_valid_position:
            self.turns += 1
            self.snake.turn('down')

    def game_over(self):
        self.is_alive = False

    @property
    def snake_in_food_position(self):
        return self.snake.pos == self.food.pos

    def _new_food(self):
        food = Food(self.canvas)
        while (
            any([parts.pos == food.pos for parts in self.snake.body]) or
                self.snake.pos == self.food.pos):
            food = Food(self.canvas)

        return food

    def snake_eats_food(self):
        self.snake.eat(self.food)
        self.food = self._new_food()
        self.score += 1

    def show_border(self):
        self.canvas.create_line(
            0,
            OFFSET - 4,
            X_SIZE + 4,
            OFFSET - 4,
            fill=BORD_COLOR,
            width=OFFSET
        )

        self.canvas.create_line(
            OFFSET - 4,
            OFFSET - 4,
            OFFSET - 4,
            Y_SIZE,
            fill=BORD_COLOR,
            width=OFFSET
        )

        self.canvas.create_line(
            X_SIZE - 4,
            OFFSET - 4,
            X_SIZE - 4,
            Y_SIZE,
            fill=BORD_COLOR,
            width=OFFSET
        )

        self.canvas.create_line(
            OFFSET - 4,
            Y_SIZE - 4,
            X_SIZE - 4,
            Y_SIZE - 4,
            fill=BORD_COLOR,
            width=OFFSET
        )

    def tick(self):
        # clear sceen
        self.canvas.delete("all")

        self.show_border()
        self.food.show()
        self.snake.show()
        self.show_score()

        if not self.snake.in_valid_position:
            self.game_over()

        if self.snake_in_food_position:
            self.snake_eats_food()

        # draw screen
        self.root.update_idletasks()
        self.root.update()

        self.snake.walk()

    def end(self):
        # terminates tkinter objects
        self.canvas.destroy()
        self.root.destroy()

    def play(self):
        # binds keyboard controls
        self.root.bind('<Left>', self.keyboard_left)
        self.root.bind('<Right>', self.keyboard_right)
        self.root.bind('<Up>', self.keyboard_up)
        self.root.bind('<Down>', self.keyboard_down)

        # main loop
        while self.is_alive:
            self.tick()
            self.playtime += HUMAN_TIMEOUT
            sleep(HUMAN_TIMEOUT)

        # on game over
        sleep(0.3)
        print('Score: ', self.score)
        self.end()


if __name__ == '__main__':
    game = Game()
    game.play()
