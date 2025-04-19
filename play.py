from game import Game, Bot
from random import randint
import pandas as pd
import argparse
import sys
import os


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--bot-snakes',
        help='Number of bot-controlled snakes',
        default=0)

    argparser.add_argument(
        '--food',
        help='Number of initial food',
        default=1)

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
        '--training-tick-rate',
        action='store',
        help='How many game ticks per second',
        default=6000)

    argparser.add_argument(
        '--performance-tick-rate',
        action='store',
        help='How many game ticks per second',
        default=30)

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
        '--training-show',
        action='store_true',
        help='Show the game interface during training')

    argparser.add_argument(
        '--no-output',
        action='store_true',
        help='Do not print any output')

    args = argparser.parse_args()
    return vars(args)


if __name__ == '__main__':
    args = get_args()

    bots = {}
    for i in range(int(args['bot_snakes'])):
        bot_name = f"{i}"
        ai_parameters = [
            0.99,  # GAMMA
            0.9,   # EPS_START
            0.05,  # EPS_END
            0.005, # TAU
        ]
        vision_length = int(args['map_x']) * int(args['map_y'])
        bot = Bot(bot_name, ai_parameters, vision_length)
        bots.update({bot_name: bot})

    # training

    i = 0
    game_points = {}
    while(True):
        try:
            print(f"Training iteration {i}:")
            game = Game(
                collision=not args['no_collision'],
                self_collision=not args['no_self_collision'],
                debug=args['debug'],
                size_x=int(args['map_x']),
                size_y=int(args['map_y']),
                tick_rate=float(args['training_tick_rate']),
                show=args['training_show'],
                food=args['food'],
                food_replace=not args['no_food_replace'],
                human=args['human'],
                bots=bots,
                bots_learn=True
            )
            game.play()
            game.print_game_state()
            game_points.update({i: {
                'score': list(game.snakes.values())[0].score,
                'time': game.playtime_ticks
            }})
            print(game_points[i])
            i += 1
        except KeyboardInterrupt:
            print(F"Training Done")
            break
    
    # example
    try:
        print(f"Performance after {i} training iterations:")
        game = Game(
            collision=not args['no_collision'],
            self_collision=not args['no_self_collision'],
            debug=args['debug'],
            size_x=int(args['map_x']),
            size_y=int(args['map_y']),
            tick_rate=float(args['performance_tick_rate']),
            show=True,
            food=args['food'],
            food_replace=not args['no_food_replace'],
            human=args['human'],
            bots=bots,
            bots_learn=False
        )
        game.play()
        game.print_game_state()
        game_points.update({i: {
            'score': list(game.snakes.values())[0].score,
            'time': game.playtime_ticks
        }})
        print(game_points[i])
    except KeyboardInterrupt:
        print(F"Performance done")
        sys.exit(0)