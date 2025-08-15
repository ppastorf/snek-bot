
import random 
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import argparse
import os
import sys

from multiprocessing import Pool

from src.ai import ai
from src.ga import Generation, Genome, GENOME_LENTH
from src.game import game

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



def create_bot(bot_name: str, bot_genome: Generation = None) -> game.Bot:
    if bot_genome == None:
        bot_genome = genome.get_random_genome()
    return game.Bot(bot_name, bot_genome.genome_array, vision_length)




def train_generation(generation: Generation):
    gen_values = generation.values()
    if len(gen_values) != generation.n_bots:
        raise Exception("Inconsistency in generation ", generation.name)

    print()
    # Training in parallel
    with Pool(processes=4) as pool:
        results = pool.map(train, data)


if __name__ == '__main__':
    args = get_args()
    vision_length = int(args['map_x']) * int(args['map_y'])

    n_bots = int(args['bot_snakes'])

    generation = 0

    # Generation 0 Bots
    gen_0_bots = {}
    for i in range(n_bots):
        bot = create_bot(f"{i}")
        gen_0_bots.update({bot.name: bot})
        if args['debug']:
            print("Created bot ", bot.name, ", using genome: ", bot.ai_parameters)
    gen_0 = Generation("Generation 0", gen_0_bots)
    
    # Generation 0 bots training
    game_points = {}
    training_episodes = int(args['training_episodes'])
    episode = 0
    while episode < training_episodes:
        try:
            print(f"Training episode {i}:")
            game_instance = game.Game(
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
                gen_0_bots=bots,
                bots_learn=True
            )
            game_instance.play()
            game_instance.print_game_state()
            game_points.update({i: {
                'episode': i,
                'score': list(game_instance.snakes.values())[0].score,
                'time': game_instance.playtime_ticks
            }})
            print(game_points[i])
            i += 1
        except KeyboardInterrupt:
            break


    # for i in range(1, args['n_generations']):
    #     gen_bots = populate(gen_0)
    #     gen = Generation(f"Generation {i}", gen_bots)


  
    
    print(f"Performance after {i} training episodes:")
    game_instance = game.Game(
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
        game_instance.play()
        game_instance.print_game_state()
        print({'score': list(game_instance.snakes.values())[0].score,'time': game_instance.playtime_ticks})
    except KeyboardInterrupt:
        game_instance.end_game()

    # print(f"Training Done")
    # n_best_scores = 5
    # best_scores = sorted(game_points.values(), key=lambda x: x['score'], reverse=True)[:n_best_scores]
    # print(f"Best scores:")
    # for score in best_scores:
    #     print(score)

    # x = [d['episode'] for d in game_points.values()]
    # time = [d['time'] for d in game_points.values()]
    # score = [d['score'] for d in game_points.values()]
    # max_time = max(time)
    # max_score = max(score)
    # avg_time = statistics.mean(time)
    # avg_score = statistics.mean(score)

    # plt.subplot(1, 2, 1)
    # plt.plot(x, score, label="Score")
    # plt.axhline(avg_score, color='orange', linestyle='--', label=f'Average = {avg_score:.2f}')
    # plt.axhline(max_score, color='red', linestyle='--', label=f'Max = {max_score:.2f}')
    # plt.title("Score")
    # plt.grid(True)
    # plt.legend()

    # plt.subplot(1, 2, 2)
    # plt.plot(x, time, label="Time")
    # plt.axhline(avg_time, color='orange', linestyle='--', label=f'Average = {avg_time:.2f}')
    # plt.axhline(max_time, color='red', linestyle='--', label=f'Max = {max_time:.2f}')
    # plt.title("Time")
    # plt.grid(True)
    # plt.legend()

    # plt.tight_layout()

    # try:
    #     plt.show()
    # except KeyboardInterrupt:
    #     sys.exit(0)