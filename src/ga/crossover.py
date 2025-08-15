import numpy as np
import uuid
import random
from typing import Self

from .genome import GENOME_LENTH, Genome

def crossover_genomes(genome_a, genome_b: Genome, crossover_type: str, alpha: float = 0.5) -> Genome:
    result_genome = []

    match crossover_type:
        case "pick":
            food_reward      = random_choice(genome_a.genome_array[0], genome_b.genome_array[0])
            playtime_reward  = random_choice(genome_a.genome_array[1], genome_b.genome_array[1])
            death_penalty    = random_choice(genome_a.genome_array[2], genome_b.genome_array[2])
            gamma            = random_choice(genome_a.genome_array[3], genome_b.genome_array[3])
            eps_start        = random_choice(genome_a.genome_array[4], genome_b.genome_array[4])
            eps_end          = random_choice(genome_a.genome_array[5], genome_b.genome_array[5])
            eps_decay        = random_choice(genome_a.genome_array[6], genome_b.genome_array[6])
            learning_rate    = random_choice(genome_a.genome_array[7], genome_b.genome_array[7])
            n_hidden_layers  = random_choice(genome_a.genome_array[8], genome_b.genome_array[8])
            hidden_layer_len = random_choice(genome_a.genome_array[9], genome_b.genome_array[9])
            result_genome = [
                food_reward,
                playtime_reward,
                death_penalty,
                gamma,
                eps_start,
                eps_end,
                eps_decay,
                learning_rate,
                n_hidden_layers,
                hidden_layer_len
            ]
        case "wheighted_avg":
            food_reward      = weighted_avg(genome_a.genome_array[0], genome_b.genome_array[0], alpha)
            playtime_reward  = weighted_avg(genome_a.genome_array[1], genome_b.genome_array[1], alpha)
            death_penalty    = weighted_avg(genome_a.genome_array[2], genome_b.genome_array[2], alpha)
            gamma            = weighted_avg(genome_a.genome_array[3], genome_b.genome_array[3], alpha)
            eps_start        = weighted_avg(genome_a.genome_array[4], genome_b.genome_array[4], alpha)
            eps_end          = weighted_avg(genome_a.genome_array[5], genome_b.genome_array[5], alpha)
            eps_decay        = weighted_avg(genome_a.genome_array[6], genome_b.genome_array[6], alpha)
            learning_rate    = weighted_avg(genome_a.genome_array[7], genome_b.genome_array[7], alpha)
            n_hidden_layers  = random_choice(genome_a.genome_array[8], genome_b.genome_array[8])
            hidden_layer_len = random_choice(genome_a.genome_array[9], genome_b.genome_array[9])
            result_genome = [
                food_reward,
                playtime_reward,
                death_penalty,
                gamma,
                eps_start,
                eps_end,
                eps_decay,
                learning_rate,
                n_hidden_layers,
                hidden_layer_len
            ]

        case _:
            raise Exception("Crossover type not implemented", crossover_type)

    if len(result_genome) != GENOME_LENTH:
        raise Exception("Failed to build a genome with", GENOME_LENTH," characters.")

    return Genome(result_genome)


####################
# Helpers
####################

def random_choice(choice_a, choice_b):
    return random.choice(choice_a, choice_b)

def weighted_avg(value_a, value_b, alpha: float) -> float:
    if not isinstance(value_a, float):
        raise Exception("Cannot do weighted average with value_a = ", value_a, ". It must be an float.")
    if not isinstance(value_b, float):
        raise Exception("Cannot do weighted average with value_b = ", value_b, ". It must be an float.")

    if alpha < 0.0 or alpha > 1.0:
        raise Exception("Cannot do weighted average with alpha = ", alpha, ". It must be between 0 and 1.")
    return (alpha * value_a) + ((1 - alpha) * value_b)
