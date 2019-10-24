from tkinter import *
from time import sleep
from . import elements as elm
from random import randrange
from pprint import pprint

MAP_SIZE = [40, 40]
SIZE_X = MAP_SIZE[0]
SIZE_Y = MAP_SIZE[1]

START_POS = [int(SIZE_X / 2), int(SIZE_Y / 2)]
START_POS_X = START_POS[0]
START_POS_Y = START_POS[1]

SCORE_SIZE = 20
PIECE_SIZE = 10

HUMAN_DELAY = 0.04
BOT_DELAY = 0.01

DEFAULT_SIZE = 10
DEFAULT_COLOR = "#aaaaaa"

BLOCK_SIZE = 10

SCORE_OFFSET = 30


class GameOver(Exception):
    pass


class Map():
    def __init__(self, size_x, size_y, board):
        self.size_x = size_x
        self.size_y = size_y
        self.board = board

    def on_position(self, x, y):
        try:
            element = self.board[x][y]
        except IndexError:
            print(x, y)
            element = None

        return element

    def set_position(self, x, y, elem_id):
        self.board[x][y] = elem_id
        return elem_id

    @staticmethod
    def init_empty_board(size_x, size_y):
        board = []
        for i in range(size_x):
            row = []
            for i in range(size_y):
                row.append(0)
            board.append(row)

        return board


class Game(object):
    def __init__(
            self,
            size_x=SIZE_X,
            size_y=SIZE_Y,
            show=True,
            tick_delay=HUMAN_DELAY,
            win_title="Snake"):

        if show:
            root = Tk()
            root.title(win_title)
            canvas = Canvas(
                root,
                width=size_x * BLOCK_SIZE,
                height=size_y * BLOCK_SIZE + SCORE_OFFSET
            )
            canvas.pack(expand=YES, fill=BOTH)
            root.bind('<Return>', self.end_game)
        else:
            root = None
            canvas = None

        self.elem_count = 0
        self.elements = {}
        self.snakes = {}

        self.size_x = size_x
        self.size_y = size_y

        self.root = root
        self.canvas = canvas

        self.tick_delay = tick_delay

        self.playtime = 0.0
        self.should_run = True

        self.map = self.parse_map_file('file')

        self.add_food('random_pos')

    def parse_map_file(self, file):
        size_x, size_y = SIZE_X, SIZE_Y

        M = Map(size_x, size_y, Map.init_empty_board(size_x, size_y))

        return M

    @staticmethod
    def human_playable():
        game = Game()

        snake1 = game.add_snake(color='blue')
        game.bind_snake_to_keys(snake1)

        return game

    @staticmethod
    def bot_playable(bot):
        game = Game()
        snake = game.add_snake()
        game.bind_snake_to_bot(snake, bot)

        return game

    def element_at(self, x, y):
        elem_id = self.map.on_position(x, y)

        if elem_id == 0:
            return None

        return self.elements[elem_id]

        return game

    def bind_snake_to_keys(self, snake):
        if snake.bind is not None:
            return

        self.root.bind('<Left>', snake.keyboard_direction)
        self.root.bind('<Right>', snake.keyboard_direction)
        self.root.bind('<Up>', snake.keyboard_direction)
        self.root.bind('<Down>', snake.keyboard_direction)
        snake.bind = "player"

    def bind_snake_to_bot(self, snake, bot):
        if snake.bind is not None:
            return

        bot.snake = snake
        snake.bind = bot
        snake.take_turn = bot.take_turn

    def new_elem_id(self):
        self.elem_count += 1
        return self.elem_count

    def add_snake(
            self,
            start_x=START_POS_X,
            start_y=START_POS_Y,
            bot=None,
            color=elm.SNAKE_COLOR,
            direction='left'):

        snake = elm.Snake(
            self, start_x, start_y, start_dir=direction, color=color
        )
        self.snakes.update({
            snake.elem_id: snake
        })
        self.elements.update({
            snake.elem_id: snake
        })

        if bot is not None:
            self.bind_snake_to_bot(snake, bot)

        return snake

    def remove_snake(self, snake):
        self.snakes.pop(snake.elem_id, None)
        self.elements.pop(snake.elem_id, None)

    def add_food(self, pos):
        if pos == 'random_pos':
            pos_x, pos_y = self.rand_free_pos()
        else:
            pos_x, pos_y = pos

        food = elm.Food(self, pos_x, pos_y)

        self.elements.update({
            food.elem_id: food
        })

        self.map.set_position(pos_x, pos_y, food.elem_id)

        return food

    def remove_food(self, food):
        self.elements.pop(food.elem_id, None)
        self.map.set_position(food.pos_x, food.pos_y, 0)

    @property
    def x_range(self):
        min_x = 0
        max_x = self.map.size_x

        return (min_x, max_x)

    @property
    def y_range(self):
        min_y = 0
        max_y = self.map.size_y

        return (min_y, max_y)

    def rand_free_pos(self):

        pos_x = randrange(*self.x_range, 1)
        pos_y = randrange(*self.y_range, 1)

        return pos_x, pos_y

    def update_elements(self):
        for e in self.elements:
            self.elements[e].update()

    def show_snake_score(self, i, snake):
            screen_size_x, screen_size_y = self.screen_map_size()

            text = "{}".format(snake.length)
            text_x = (screen_size_x / (len(self.snakes) + 1)) * (i + 1)
            text_y = screen_size_y + (SCORE_OFFSET / 2)

            head_x = text_x - (len(text) + 20)
            head_y = screen_size_y + (SCORE_OFFSET / 2) - (snake.head.size / 2)

            self.show_element(snake.head, pos=(head_x, head_y))

            self.canvas.create_text(
                text_x, text_y,
                text=text
            )

    def show_score(self):
        screen_size_x, screen_size_y = self.screen_map_size()
        border_width = 4
        border_x = [0, screen_size_x]
        border_y = screen_size_y + border_width

        self.canvas.create_line(
            border_x[0],
            border_y,
            border_x[1],
            border_y,
            fill="#aaa1aa",
            width=border_width
        )

        for i, snake in enumerate(self.snakes.values()):
            self.show_snake_score(i, snake)

    def screen_map_size(self):
        x_size = self.map.size_x * BLOCK_SIZE
        y_size = self.map.size_y * BLOCK_SIZE

        return x_size, y_size

    def pos_on_screen(self, x, y):
        return x * BLOCK_SIZE, y * BLOCK_SIZE

    def show_element(self, element, pos=None):

        if pos is None:
            pos_x, pos_y = self.pos_on_screen(element.pos_x, element.pos_y)
        else:
            pos_x, pos_y = pos[0], pos[1]

        self.canvas.create_rectangle(
            pos_x, pos_y,
            pos_x + element.size,
            pos_y + element.size,
            fill=element.color
        )

    def draw_screen(self):
        self.show_score()

        for e in self.elements.values():
            e.show()

        self.root.update_idletasks()
        self.root.update()

    def clear_screen(self):
        self.canvas.delete("all")

    def check_if_game_ends(self):
        if not any([snake.is_alive for snake in self.snakes.values()]):
            raise GameOver

    def tick(self):
        self.clear_screen()
        self.update_elements()
        self.check_if_game_ends()
        self.draw_screen()

    def end_game(self, event):
        self.should_run = False

    def end(self):
        sleep(0.3)
        self.canvas.destroy()
        self.root.destroy()

    @property
    def game_state(self):
        return {
            "elements": [self.elements[e].state for e in self.elements]
        }

    def play(self):
        while self.should_run:
            try:
                self.tick()
                sleep(self.tick_delay)
            except GameOver:
                self.should_run = False

        self.end()
