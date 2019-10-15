from tkinter import *
from time import sleep
from . import elements as elm

X_SIZE = 400
Y_SIZE = 400

BORDER_SIZE = 10

SCORE_SIZE = 20
PIECE_SIZE = 10


START_POS = [300, 200]
START_POS_X = START_POS[0]
START_POS_Y = START_POS[1]
START_DIR = 'left'

HUMAN_DELAY = 0.04
BOT_DELAY = 0.01

BORDER_COLOR = "#000000"


class Game(object):

    def __init__(
            self,
            x_size=X_SIZE,
            y_size=Y_SIZE,
            show=True,
            delay=HUMAN_DELAY,
            win_title="Snake"):

        if show:
            root = Tk()
            root.title(win_title)
            canvas = Canvas(
                root,
                width=x_size,
                height=y_size + SCORE_SIZE
            )
            canvas.pack(expand=YES, fill=BOTH)
            root.bind('<Return>', self.end_game)
        else:
            root = None
            canvas = None

        self.elements = {}

        self.x_size = x_size
        self.y_size = y_size

        self.playable_x = [BORDER_SIZE, self.x_size - BORDER_SIZE]
        self.playable_y = [BORDER_SIZE, self.y_size - BORDER_SIZE]

        self.root = root
        self.canvas = canvas

        self.tick_delay = delay

        self.add_snake(elm.Snake(self, START_POS_X, START_POS_Y))

        self.add_food(elm.Food(self))

        self.score = 0
        self.playtime = 0.0

    @staticmethod
    def human_playable():
        game = Game()
        game.snake.bind_to_keys()

        return game

    @staticmethod
    def bot_playable(bot):
        game = Game()
        game.snake.bind_to_bot(bot)

        return game

    def add_snake(self, snake):
        self.snake = snake
        self.elements.update({
            "snake": snake
        })

    def add_food(self, food):
        self.food = food
        self.elements.update({
            "food": food
        })

    def remove_food(self):
        self.elements.pop("food", None)
        del self.food

    def show_score(self):
        self.canvas.create_text(
            X_SIZE / 2,
            Y_SIZE + BORDER_SIZE,
            text='Score: {}'.format(self.score))

    def end_game(self, event):
        self.kill_snake()

    def kill_snake(self):
        self.snake.is_alive = False

    @property
    def snake_in_food_position(self):
        return self.snake.pos == self.food.pos

    def new_food(self):
        food = elm.Food(self)

        while (
            any([parts.pos == food.pos for parts in self.snake.tail]) or
                self.snake.pos == food.pos):
            food = elm.Food(self)

        return food

    def snake_eats_food(self):
        self.snake.eat()
        self.remove_food()
        self.add_food(self.new_food())
        self.score += 1

    def show_border(self, color=BORDER_COLOR, size=BORDER_SIZE):
        self.canvas.create_line(
            0,
            size - 4,
            self.x_size + 4,
            size - 4,
            fill=color,
            width=size
        )

        self.canvas.create_line(
            size - 4,
            size - 4,
            size - 4,
            self.y_size,
            fill=color,
            width=size
        )

        self.canvas.create_line(
            self.x_size - 4,
            size - 4,
            self.x_size - 4,
            self.y_size,
            fill=color,
            width=size
        )

        self.canvas.create_line(
            size - 4,
            self.y_size - 4,
            self.x_size - 4,
            self.y_size - 4,
            fill=color,
            width=size
        )

    def draw_screen(self):
        self.show_border()
        self.show_score()

        for e in self.elements:
            self.elements[e].show()

        self.root.update_idletasks()
        self.root.update()

    def clear_screen(self):
        self.canvas.delete("all")

    def update_elements(self):
        for e in self.elements:
            self.elements[e].update()

    def tick(self):
        self.clear_screen()
        self.update_elements()

        if not self.snake.in_valid_position:
            self.snake.die()
            return

        if self.snake_in_food_position:
            self.snake_eats_food()

        self.draw_screen()
        # self.snake.turn()

    def end(self):
        sleep(0.3)
        self.canvas.destroy()
        self.root.destroy()

    @property
    def game_state(self):
        return {
            "score": self.score,
            "elements": [{e: self.elements[e].state} for e in self.elements]
        }

    def play(self):
        while self.snake.is_alive:
            self.tick()
            sleep(self.tick_delay)

        self.end()
