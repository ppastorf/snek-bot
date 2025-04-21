from game import Game, Bot
import random 
import pandas as pd
import statistics
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
            # food_reward (1 - 100)
            random.uniform(1, 100.0),

            # playtime_reward (1 - 100)
            random.uniform(1, 100.0),

            # death_penalty (1 - 100)
            random.uniform(1, 100.0),

            # gamma (0 - 1)
            random.uniform(0, 1.0),

            # eps_start (0 - 1 upper)
            random.uniform(0.5, 0.99),

            # eps_end  (0 - 1 lower)
            random.uniform(1e-4, 0.5),

            # eps_decay (1000 - 100000)
            random.uniform(1000, 100000),

            # learning_rate (0,1e-1)
            random.uniform(0.0, 1e-1),

            # n_hidden_layers
            # random.choice([1,2]),
            1,

            # hidden_layer_len
            # random.choice([32, 64, 128, 256, 512, 1024]),
            128,
        ]
        print("Using AI parameters:")
        print(ai_parameters)
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
    try:
        game.play()
        game.print_game_state()
        print({'score': list(game.snakes.values())[0].score,'time': game.playtime_ticks})
    except KeyboardInterrupt:
        game.end_game()

    print(f"Training Done")
    n_best_scores = 5
    best_scores = sorted(game_points.values(), key=lambda x: x['score'], reverse=True)[:n_best_scores]
    print(f"Best scores:")
    for score in best_scores:
        print(score)

    x = [d['episode'] for d in game_points.values()]
    time = [d['time'] for d in game_points.values()]
    score = [d['score'] for d in game_points.values()]
    avg_time = statistics.mean(time)
    max_score = max(score)
    avg_score = statistics.mean(score)

    plt.subplot(1, 2, 1)
    plt.plot(x, score, label="Score")
    plt.axhline(avg_score, color='orange', linestyle='--', label=f'Average = {avg_score:.2f}')
    plt.axhline(max_score, color='red', linestyle='--', label=f'Max = {max_score:.2f}')
    plt.title("Score")
    plt.grid(True)
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(x, time, label="Time")
    plt.axhline(avg_time, color='orange', linestyle='--', label=f'Average = {avg_time:.2f}')
    plt.title("Time")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    try:
        plt.show()
    except KeyboardInterrupt:
        sys.exit(0)