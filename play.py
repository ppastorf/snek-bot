from game import Game, Bot
from random import randint
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import os


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--bot-snakes',
        help='Number of bot-controlled snakes',
        default=1)

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
        help='How many game ticks per second during training',
        default=6000)

    argparser.add_argument(
        '--training-episodes',
        action='store',
        help='How many training episodes',
        default=1000)

    argparser.add_argument(
        '--performance-tick-rate',
        action='store',
        help='How many game ticks per second on performance',
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
    game_points = {}
    i = 0
    while i < int(args['training_episodes']):
        try:
            print(f"Training episode {i}:")
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
                'episode': i,
                'score': list(game.snakes.values())[0].score,
                'time': game.playtime_ticks
            }})
            print(game_points[i])
            i += 1
        except KeyboardInterrupt:
            break
    
    # example
    try:
        print(f"Performance after {i} training episodes:")
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
            'episode': i,
            'score': list(game.snakes.values())[0].score,
            'time': game.playtime_ticks
        }})
        print(game_points[i])
    except KeyboardInterrupt:
        sys.exit(0)

    print(f"Training Done")
    n_best_scores = 5
    best_scores = sorted(game_points.values(), key=lambda x: x['score'], reverse=True)[:n_best_scores]
    print(f"Best scores:")
    for score in best_scores:
        print(score)

    x1 = [d['episode'] for d in game_points.values()]
    y1 = [d['time'] for d in game_points.values()]
    plt.plot(x1, y1, marker='.', label='Time')

    x2 = [d['episode'] for d in game_points.values()]
    y2 = [d['score'] for d in game_points.values()]
    plt.plot(x2, y2, marker='.', label='Score')

    plt.xlabel("Episode")
    plt.ylabel("Value")
    plt.title(f"Snek bot after {i} training episodes")
    plt.legend()
    plt.grid(True)
    plt.show()
