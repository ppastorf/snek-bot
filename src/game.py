from tkinter import *
from time import sleep
import snake as sn

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
            root.bind('<Return>', self.keyboard_return)
        else:
            root = None
            canvas = None

        self.elements = []

        self.x_size = x_size
        self.y_size = y_size

        self.playable_x = [BORDER_SIZE, self.x_size - BORDER_SIZE]
        self.playable_y = [BORDER_SIZE, self.y_size - BORDER_SIZE]

        self.root = root
        self.canvas = canvas

        self.tick_delay = delay

        self.snake = sn.Snake(self, START_POS_X, START_POS_Y)
        self.add_element(self.snake)

        self.food = sn.Food(self)
        self.add_element(self.food)

        self.score = 0
        self.playtime = 0.0
        self.is_alive = True

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

    def add_element(self, element):
        self.elements.append(element)

    def show_score(self):
        self.canvas.create_text(
            X_SIZE / 2,
            Y_SIZE + BORDER_SIZE,
            text='Score: {}'.format(self.score))

    def keyboard_event(self, event):
        direction = event.keysym.lower()
        self.snake.turn(direction)

    def keyboard_return(self, event):
        self.game_over()

    def game_over(self):
        self.is_alive = False

    @property
    def snake_in_food_position(self):
        return self.snake.pos == self.food.pos

    def _new_food(self):
        del self.food
        food = sn.Food(self)

        while (
            any([parts.pos == food.pos for parts in self.snake.tail]) or
                self.snake.pos == food.pos):
            food = sn.Food(self)

        return food

    def snake_eats_food(self):
        self.snake.eat()
        self.food = self._new_food()
        self.add_element(self.food)
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

        for element in self.elements:
            element.show()

        self.root.update_idletasks()
        self.root.update()

    def clear_screen(self):
        self.canvas.delete("all")

    def update_elements(self):
        for element in self.elements:
            element.update()

    def tick(self):
        self.clear_screen()
        self.update_elements()

        if not self.snake.in_valid_position:
            self.game_over()
            return

        if self.snake_in_food_position:
            self.snake_eats_food()

        self.draw_screen()

    def end(self):
        sleep(0.3)
        print('Score: ', self.score)
        self.canvas.destroy()
        self.root.destroy()

    def game_state(self):
        # TODO
        pass

    def play(self):
        while self.is_alive:
            self.tick()
            sleep(self.tick_delay)

        self.end()


if __name__ == '__main__':
    game = Game.human_playable()
    game.play()
