from game import Game
from random import randint
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
        dir_index = randint(0, len(self.dir_map.keys()) - 1)
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
        '--map-x',
        action='store',
        help='Map x size',
        default=50)

    argparser.add_argument(
        '--tick-delay',
        action='store',
        help='TIme between every game tick in seconds',
        default=0.04)

    argparser.add_argument(
        '--map-y',
        action='store',
        help='Map y size',
        default=50)

    argparser.add_argument(
        '--no-food-replace',
        action='store_true',
        help='Do not replace food when eaten')

    argparser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info')

    argparser.add_argument(
        '--no-show',
        action='store_true',
        help='Do not show the game interface')

    argparser.add_argument(
        '--no-output',
        action='store_true',
        help='Do not print any output')

    args = argparser.parse_args()
    return vars(args)


if __name__ == '__main__':
    args = get_args()
    game = Game(
        collision=not args['no_collision'],
        self_collision=not args['no_self_collision'],
        debug=args['debug'],
        size_x=int(args['map_x']),
        size_y=int(args['map_y']),
        tick_delay=float(args['tick_delay']),
        show=not args['no_show']
    )

    if args['human']:
        snake = game.add_snake(
            int(game.size_x / 2), int(game.size_y / 2))
        game.bind_snake_to_keys(snake)

    for i in range(int(args['snakes'])):
        bot = Bot(name='aa')
        game.add_snake(
            i * 3, i * 3,
            bot=bot,
        )

    for i in range(int(args['food'])):
        food = game.add_food('random_pos', replace=not args['no_food_replace'])

    game.play()

    if not args['no_output']:
        print(game.game_state.to_string(index=False))
