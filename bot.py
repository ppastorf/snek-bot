from game import Game
from random import randrange
import pandas as pd
import argparse


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


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--snakes',
        help='Number of bot-controlled snakes',
        default=10)

    argparser.add_argument(
        '--food',
        help='Number of initial food',
        default=300)

    argparser.add_argument(
        '--no-self-collision',
        action='store_true',
        help='Snakes do not die on self hit')

    argparser.add_argument(
        '--no-collision',
        action='store_true',
        help='Snakes do not die when hitting each other')

    argparser.add_argument(
        '--human',
        action='store_true',
        help='Add an keyboard controlled snake')

    argparser.add_argument(
        '--no-food-replace',
        action='store_true',
        help='Do not replace food when eaten')
    args = argparser.parse_args()

    return vars(args)


if __name__ == '__main__':
    args = get_args()
    game = Game()

    if args['human']:
        snake = game.add_snake(color=new_color())
        game.bind_snake_to_keys(snake)

    for i in range(int(args['snakes'])):
        bot = Bot(name=new_color())
        game.add_snake(bot=bot, color=bot.name)

    for i in range(int(args['food'])):
        food = game.add_food('random_pos', replace=not args['no_food_replace'])

    game.play()

    print(game.game_state.to_string(index=False))
