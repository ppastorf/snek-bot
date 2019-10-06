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

        self.x_size = x_size
        self.y_size = y_size

        self.playable_x = [BORDER_SIZE, self.x_size - BORDER_SIZE]
        self.playable_y = [BORDER_SIZE, self.y_size - BORDER_SIZE]

        self.root = root
        self.canvas = canvas

        self.tick_delay = delay

        self.snake = sn.Snake(self, START_POS_X, START_POS_Y)
        self.food = sn.Food(self)

        self.score = 0
        self.playtime = 0.0
        self.is_alive = True

    @staticmethod
    def human_playable():
        game = Game()
        game.bind_to_keys()

        return game

    def show_score(self):
        self.canvas.create_text(
            X_SIZE / 2,
            Y_SIZE + BORDER_SIZE,
            text='Score: {}'.format(self.score))

    def keyboard_left(self, event):
        self.snake.turn('left')

    def keyboard_right(self, event):
        self.snake.turn('right')

    def keyboard_up(self, event):
        self.snake.turn('up')

    def keyboard_down(self, event):
        self.snake.turn('down')

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
            any([parts.pos == food.pos for parts in self.snake.body]) or
                self.snake.pos == food.pos):
            food = sn.Food(self)

        return food

    def snake_eats_food(self):
        self.snake.eat()
        self.food = self._new_food()
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
        self.root.update_idletasks()
        self.root.update()

    def clear_screen(self):
        self.canvas.delete("all")

    def tick(self):
        self.clear_screen()
        self.show_border()
        self.show_score()
        self.food.show()
        self.snake.show()

        if not self.snake.in_valid_position:
            self.game_over()
            return

        if self.snake_in_food_position:
            self.snake_eats_food()

        self.snake.walk()
        self.draw_screen()

    def end(self):
        sleep(0.3)
        print('Score: ', self.score)
        self.canvas.destroy()
        self.root.destroy()

    def bind_to_keys(self):
        self.root.bind('<Left>', self.keyboard_left)
        self.root.bind('<Right>', self.keyboard_right)
        self.root.bind('<Up>', self.keyboard_up)
        self.root.bind('<Down>', self.keyboard_down)

    def play(self):
        while self.is_alive:
            self.tick()
            self.snake.time_alive += self.tick_delay
            sleep(self.tick_delay)

        self.end()


if __name__ == '__main__':
    game = Game.human_playable()
    game.play()


    @property
    def game_state(self):
        # distance to wall to the front, left and right
        dist_left = (self.snake.pos_x - BORDER_SIZE) / REAL_X_SIZE
        dist_up = (self.snake.pos_y - BORDER_SIZE) / REAL_Y_SIZE
        dist_right = 1 - dist_left
        dist_down = 1 - dist_up

        if self.snake.direction == 'left':
            walldist_front = dist_left
            walldist_left = dist_down
            walldist_right = dist_up

        if self.snake.direction == 'right':
            walldist_front = dist_right
            walldist_left = dist_up
            walldist_right = dist_down

        if self.snake.direction == 'up':
            walldist_front = dist_up
            walldist_left = dist_left
            walldist_right = dist_right

        if self.snake.direction == 'down':
            walldist_front = dist_down
            walldist_left = dist_right
            walldist_right = dist_left

        # angle to food (normalized)
        food_angle_rad = atan2(self.snake.pos_y - self.food.pos_y,
                               self.snake.pos_x - self.food.pos_x)
        food_angle = degrees(food_angle_rad) / 180

        return [walldist_front, walldist_left, walldist_right, food_angle]

#     def control_snake(self, action):
#         if action == 'straight':
#             pass
#         else:
#             if self.snake.direction == 'left':
#                 if action == 'left':
#                     self.keyboard_down(None)
#                 if action == 'right':
#                     self.keyboard_up(None)

#             elif self.snake.direction == 'right':
#                 if action == 'left':
#                     self.keyboard_up(None)
#                 if action == 'right':
#                     self.keyboard_down(None)

#             elif self.snake.direction == 'up':
#                 if action == 'left':
#                     self.keyboard_left(None)
#                 if action == 'right':
#                     self.keyboard_right(None)

#             elif self.snake.direction == 'down':
#                 if action == 'left':
#                     self.keyboard_right(None)
#                 if action == 'right':
#                     self.keyboard_left(None)

#     def tick(self):
#         self.canvas.delete("all")

#         self.show_border()
#         self.food.show()
#         self.snake.show()
#         self.show_score()

#         if not self.snake.in_valid_position:
#             self.game_over()
#             return

#         if self.snake_has_eaten_food:
#             self.score_up()

#         self.bot.learn_state(self.game_state)
#         action = self.bot.take_action()

#         self.control_snake(action)

#         self.root.update_idletasks()
#         self.root.update()

#         self.snake.walk()