from game import Game
from pprint import pprint
from random import randrange
import pandas as pd


class Bot(object):

    def __init__(self, snake=None, name="robson"):
        self.name = name
        self.snake = snake

        self.dir_map = {
            0: 'left',
            1: 'right',
            2: 'up',
            3: 'down'
        }

    def take_turn(self):
        dir_index = randrange(0, len(self.dir_map.keys()), 1)
        direction = self.dir_map[dir_index]
        self.snake.next_dir = direction

        return direction

    @property
    def info(self):
        values = {
            "name": self.name,
            "bind": self.snake.elem_id
        }

        state = pd.Series(data=values)
        return state


if __name__ == '__main__':

    bot1 = Bot()
    game = Game.bot_playable(bot1)

    bot2 = Bot()
    snake2 = game.add_snake(bot=bot2, color='red')

    bot3 = Bot()
    snake3 = game.add_snake(bot=bot3, color='yellow')

    for i in range(30):
        food = game.add_food('random_pos')

    game.play()

    print(game.game_state.to_string(index=False))
