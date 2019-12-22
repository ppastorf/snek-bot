from game import Game
from random import randrange
import pandas as pd


class Bot(object):

    def __init__(self, name="bot"):
        self.name = name
        self.snake = None

        self.dir_map = {
            0: 'left',
            1: 'right',
            2: 'up',
            3: 'down'
        }

    def take_turn(self):
        dir_index = randrange(0, len(self.dir_map.keys()), 1)
        self.snake.next_dir = self.dir_map[dir_index]

        return self.snake.next_dir

    @property
    def info(self):
        values = {
            "name": self.name,
            "bind": self.snake.elem_id
        }

        state = pd.Series(data=values)
        return state


def new_color():
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

    color = new_color.count % len(COLORS)
    new_color.count += 1
    return COLORS[color]


new_color.count = 0


if __name__ == '__main__':
    game = Game()

    N_SNAKES = 20

    N_FOOD = 300
    FOOD_RESPAWN = True

    for i in range(N_SNAKES):
        bot = Bot(name=new_color())
        game.add_snake(bot=bot, color=bot.name)

    for i in range(N_FOOD):
        food = game.add_food('random_pos', respawn=FOOD_RESPAWN)

    game.play()

    print(game.game_state.to_string(index=False))
