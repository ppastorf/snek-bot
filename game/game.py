import os
from tkinter import *
from time import sleep
from . import elements as elm
from . import ai as ai
import pprint
from random import randint
import pandas as pd


DEFAULT_X = 50
DEFAULT_Y = 50

TICK_DELAY = 0.04

ELEMENT_SIZE = 10
DEFAULT_SIZE = 10
DEFAULT_COLOR = "#aaaaaa"


BLOCK_SIZE = 10

SCORE_OFFSET = 30

class GameOver(Exception):
    pass


class HumanBind(object):
    def __init__(self):
        self.name = 'human'


class Bot(object):
    def __init__(self, name: str, ai_parameters: list, activations_length: int):
        self.game = None
        self.name = name
        self.snake = None
        self.ai = ai.BotAI(self, ai_parameters, activations_length)

    def take_turn(self):
        choice = self.ai.choose_action(self.snake.vision).value
        if choice != 'pass':
            next_dir = choice
        else:
            next_dir = self.snake.direction
        self.snake.next_dir = next_dir
        return next_dir
        
    def set_game(self, game):
        self.game = game

    @property
    def info(self):
        values = {
            "name": self.name,
            "bind": self.snake.elem_id
        }

        state = pd.Series(data=values)
        return state


class Map():
    def __init__(self, size_x, size_y, board):
        self.size_x = size_x
        self.size_y = size_y
        self.board = board

    def on_position(self, x, y):
        try:
            element = self.board[x][y]
        except IndexError:
            raise Exception(f"ERROR: could not get element at {x}, {y}: out of game board")

        return element

    def set_position(self, x, y, elem_id):
        self.board[x][y] = elem_id

        return elem_id

    def print(self):
        board_df = pd.DataFrame(data=self.board)
        with pd.option_context(
                'display.max_rows',
                None,
                'display.max_columns',
                None):
            print(board_df)
            print()

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
            size_x=DEFAULT_X,
            size_y=DEFAULT_Y,
            show=True,
            tick_delay=TICK_DELAY,
            collision=True,
            self_collision=True,
            debug=False,
            food=1,
            food_replace=True,
            human=True,
            bots=[],
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

            def no_op():
                pass

            self.clear_screen = no_op
            self.draw_screen = no_op
            self.end = no_op

        self.elem_count = 0
        self.elements = {}
        self.snakes = {}
        self.bots = {}

        self.size_x = size_x
        self.size_y = size_y

        self.root = root
        self.canvas = canvas

        self.tick_delay = tick_delay

        self.collision = collision
        self.self_collision = self_collision

        self.playtime_ticks = 0
        self.should_run = True

        self.map = self.parse_map_file('file')

        self.debug = debug
        self.color_count = 0

        self.food = food

        ## walls
        for i in range(self.size_x):
            self.add_wall((i, 0))
            self.add_wall((i, size_y-1))

        for i in range(self.size_y):
            self.add_wall((0, i))
            self.add_wall((size_x-1, i))

        ## bots
        for bot in bots.values():
            self.add_bot_player(bot, 'random_pos')

        ## player
        if human:
            snake = self.add_snake(
                "H0",
                int(self.size_x / 2), int(self.size_y / 2))
            self.bind_snake_to_keys(snake)

        ## food
        for i in range(int(food)):
            self.add_food('random_pos', replace=food_replace)

    def new_color(self):
        COLORS = [
            'red',
            'blue',
            'yellow',
            'pink',
            'violet',
            'orange',
            'gray',
            'maroon'
        ]
        color = self.color_count % len(COLORS)
        self.color_count += 1
        return COLORS[color]

    def parse_map_file(self, file):
        size_x, size_y = self.size_x, self.size_y

        M = Map(size_x, size_y, Map.init_empty_board(size_x, size_y))

        return M

    def element_at(self, x: int, y: int):
        elem_id = self.map.on_position(x, y)

        if elem_id == 0:
            return None

        return self.elements[elem_id]

    def bind_snake_to_keys(self, snake):
        if snake.bind is not None:
            return

        self.root.bind('<Left>', snake.keyboard_direction)
        self.root.bind('<Right>', snake.keyboard_direction)
        self.root.bind('<Up>', snake.keyboard_direction)
        self.root.bind('<Down>', snake.keyboard_direction)

        snake.bind = HumanBind()

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
            name,
            start_x,
            start_y,
            bot=None,
            color=None,
            start_length=1,
            direction='left'):

        if color is None:
            color = self.new_color()

        snake = elm.Snake(
            self,
            name,
            start_x,
            start_y,
            start_dir=direction,
            color=color,
            start_length=start_length
        )
        

        self.snakes.update({
            snake.elem_id: snake
        })

        if bot is not None:
            self.bind_snake_to_bot(snake, bot)

        return snake

    def add_bot_player(self, bot, pos):
        if pos == 'random_pos':
            pos_x, pos_y = self.rand_free_pos()
        else:
            pos_x, pos_y = pos
        self.bots.update({bot.name: bot})
        self.add_snake(
            bot.name,
            pos_x, pos_y,
            bot=bot,
        )
        bot.set_game(self)
        return bot

    def add_food(self, pos, replace=True):
        if pos == 'random_pos':
            pos_x, pos_y = self.rand_free_pos()
        else:
            pos_x, pos_y = pos
        print(f"Creating new food at position {pos_x}, {pos_y}...")
        return elm.Food(self, pos_x, pos_y, replace=replace)

    def add_wall(self, pos):
        pos_x, pos_y = pos
        return elm.Wall(self, pos_x, pos_y)

    @property
    def x_range(self):
        min_x = 0
        max_x = self.map.size_x

        return (min_x, max_x - 1)

    @property
    def y_range(self):
        min_y = 0
        max_y = self.map.size_y

        return (min_y, max_y - 1)

    def rand_free_pos(self):
        x = randint(*self.x_range)
        y = randint(*self.y_range)
        while self.map.on_position(x, y) != 0:
            x = randint(*self.x_range)
            y = randint(*self.y_range)

        print(f"position {x},{y} is free")
        return x, y

    def update_elements(self):
        for s in self.snakes.values():
            if s.is_alive:
                s.update()

    def show_snake_score(self, snake):
            screen_size_x, screen_size_y = self.screen_map_size()

            points = ":  {}".format(snake.length)
            points_x = (screen_size_x / (len(self.snakes) + 1)) * (snake.index + 1)
            points_y = screen_size_y + (SCORE_OFFSET / 2)

            head_x = points_x - 20
            head_y = screen_size_y + (SCORE_OFFSET / 2) - (snake.head.size / 2)


            if not snake.is_alive:
                snake_name = "{} (X)".format(snake.index)
            else:
                if snake.bind.name == "human":
                    snake_name = "{} (H)".format(snake.index)
                else:
                    snake_name = "{} (B)".format(snake.index)

            snake_name_x = head_x - 20
            snake_name_y = points_y

            self.show_element(snake.head, pos=(head_x, head_y))
            self.canvas.create_text(
                snake_name_x, snake_name_y,
                text=snake_name
            )
            self.canvas.create_text(
                points_x, points_y,
                text=points
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
            self.show_snake_score(snake)

    def screen_map_size(self):
        x_size = self.map.size_x * BLOCK_SIZE
        y_size = self.map.size_y * BLOCK_SIZE

        return x_size, y_size

    def pos_on_screen(self, x, y):
        return x * BLOCK_SIZE, y * BLOCK_SIZE

    def show_element(self, element, pos=None, text=None):
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
        if text != None:
            self.canvas.create_text(
            pos_x + element.size/2,
            pos_y + element.size/2,
            text=text,
            fill="#FFFFFF"
            )

    def draw_screen(self):
        self.show_score()

        for e in self.elements.values():
            if e.elem_type == "head":
                self.show_element(e, text=e.master.index)
            else:
                self.show_element(e)

        self.root.update_idletasks()
        self.root.update()


    def clear_term(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear_screen(self):
        self.canvas.delete("all")

    def check_if_game_ends(self):
        if not any([snake.is_alive for snake in self.snakes.values()]):
            raise GameOver

    def print_debug_info(self):

        print('food:')
        for e in self.elements.values():
            if e.elem_type == 'food':
                print(f"{e.elem_id} - [{e.pos_x}, {e.pos_y}]")

        print('snakes:')
        for s in self.snakes.values():
            if s.is_alive:
                sn = [s.head.elem_id]
                for t in s.tail:
                    sn.append(t.elem_id)
                print(sn)

        self.map.print()

    def train_ai_components(self):
        for bot in self.bots.values():
            bot.ai.record_transition_and_train(bot.snake.vision)

    def tick(self):
        # self.clear_term()
        self.clear_screen()
        self.update_elements()
        self.check_if_game_ends()
        self.draw_screen()
        print(self.game_state.to_string(index=False))
        if self.debug:
            self.print_debug_info()
        self.playtime_ticks += 1
        self.train_ai_components()

    def end_game(self, event):
        self.should_run = False

    def end(self):
        sleep(0.3)
        self.canvas.destroy()
        self.root.destroy()

    @property
    def game_state(self):
        states = [e.state for e in self.snakes.values()]
        state = pd.concat(states, axis=1, sort=False).transpose()

        return state

    def play(self):
        while self.should_run:
            try:
                self.tick()
                sleep(self.tick_delay)
            except GameOver:
                self.should_run = False

        self.end()
