import numpy as np
import uuid
import random
from typing import Self


####################
# Globals
####################
GENOME_LENTH = 10

####################
# Genome
####################
class Genome(object):
    id: str
    genome_array: list

    def __init__(self, array):
        self.id = uuid.uuid4()
        self.genome_array = array

    def mutate(self):
        gene_mutated = random.randint(0, len(self.genome_array))
        match gene_mutated:
            case 0:
                mutation_value = rand_food_reward()
            case 1:
                mutation_value = rand_playtime_reward()
            case 2:
                mutation_value = rand_death_penalty()
            case 3:
                mutation_value = rand_gamma()
            case 4:
                mutation_value = rand_eps_start()
            case 5:
                mutation_value = rand_eps_end()
            case 6:
                mutation_value = rand_eps_decay()
            case 7:
                mutation_value = rand_learning_rate()
            case 8:
                mutation_value = rand_n_hidden_layers()
            case 9:
                mutation_value = rand_hidden_layer_len()
            case _:
                mutation_value = self.genome_array[gene_mutated]
        self.genome_array[gene_mutated] = mutation_value


#############
# Randomness
#############
def rand_food_reward() -> float:
    return random.uniform(1, 100.0)

def rand_playtime_reward() -> float:
    return random.uniform(1, 100.0)

def rand_death_penalty() -> float:
    return random.uniform(1, 100.0)

def rand_gamma() -> float:
    return random.uniform(0, 1.0)

def rand_eps_start() -> float:
    return random.uniform(0.5, 0.99)

def rand_eps_end() -> float:
    return random.uniform(1e-4, 0.5)

def rand_eps_decay() -> float:
    return random.uniform(1000, 100000)

def rand_learning_rate() -> float:
    return random.uniform(0.0, 1e-1)

def rand_n_hidden_layers() -> float:
    return random.choice([1])

def rand_hidden_layer_len() -> float:
   return random.choice([32, 64, 128, 256, 512, 1024])

def get_random_genome() -> Genome:
    genome = [
        rand_food_reward(),
        rand_playtime_reward(),
        rand_death_penalty(),
        rand_gamma(),
        rand_eps_start(),
        rand_eps_end(),
        rand_eps_decay(),
        rand_learning_rate(),
        rand_n_hidden_layers(),
        rand_hidden_layer_len()
    ]
    return Genome(genome)
