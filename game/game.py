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
            tick_delay=HUMAN_DELAY,
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

        self.elem_count = 0
        self.elements = {}
        self.snakes = {}
        self.foods = {}
        self.main_snake = None

        self.x_size = x_size
        self.y_size = y_size

        self.playable_x = [BORDER_SIZE, self.x_size - BORDER_SIZE]
        self.playable_y = [BORDER_SIZE, self.y_size - BORDER_SIZE]

        self.root = root
        self.canvas = canvas

        self.tick_delay = tick_delay

        self.add_snake(main=True)
        self.add_food()
        self.add_food()

        self.score = 0
        self.playtime = 0.0
        self.should_run = True

    @staticmethod
    def human_playable():
        game = Game()
        game.main_snake.bind_to_keys()

        return game

    @staticmethod
    def bot_playable(bot):
        game = Game()
        game.main_snake.bind_to_bot(bot)

        return game

    def new_elem_id(self):
        self.elem_count += 1
        return self.elem_count

    def add_snake(self, main=False):
        snake = elm.Snake(self, START_POS_X, START_POS_Y, is_main=main)

        if main and self.main_snake is None:
            self.main_snake = snake

        self.snakes.update({
            snake.elem_id: snake
        })
        self.elements.update({
            snake.elem_id: snake
        })

    def remove_snake(self, snake):
        self.snakes.pop(snake.elem_id, None)
        self.elements.pop(snake.elem_id, None)
        del snake

    def add_food(self):
        food = elm.Food(self)

        self.foods.update({
            food.elem_id: food
        })
        self.elements.update({
            food.elem_id: food
        })

    def remove_food(self, food):
        self.foods.pop(food.elem_id, None)
        self.elements.pop(food.elem_id, None)
        del food

    def new_food(self):
        food = elm.Food(self)

        while (
            any([parts.pos == food.pos for parts in self.main_snake.tail]) or
                self.main_snake.pos == food.pos):
            food = elm.Food(self)

        return food

    def show_score(self):
        self.canvas.create_text(
            X_SIZE / 2,
            Y_SIZE + BORDER_SIZE,
            text='Score: {}'.format(self.score))

    def end_game(self, event):
        self.should_run = False

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

    def snake_eats_food(self, food):
        self.main_snake.eat()
        self.remove_food(food)
        self.add_food()
        self.score += 1

    def tick(self):
        # try:
            self.clear_screen()
            self.update_elements()

            self.draw_screen()

        # except Exception:
        #     self.should_run = False
        #     return

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
        while self.should_run:
            self.tick()
            sleep(self.tick_delay)

        self.end()
