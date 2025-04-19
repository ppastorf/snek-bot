import numpy as np
import random

def mutate(genome, rate=0.01, scale=0.1):
    new_genome = genome.clone()
    for i in range(len(new_genome)):
        if random.random() < rate:
            new_genome[i] += torch.randn(1).item() * scale
    return new_genome

def crossover(g1, g2):
    mask = torch.rand(len(g1)) > 0.5
    child = g1.clone()
    child[mask] = g2[mask]
    return child

def evaluate_fitness(model, data, labels):
    with torch.no_grad():
        preds = model(data).argmax(dim=1)
        return (preds == labels).float().mean().item()

POP_SIZE = 50
N_GENERATIONS = 100

def evolve(input_size, hidden_size, output_size, data, labels):
    # Initialize population
    base_model = DecisionModel(input_size, hidden_size, output_size)
    genome_size = len(get_genome(base_model))
    population = [torch.randn(genome_size) for _ in range(POP_SIZE)]

    for gen in range(N_GENERATIONS):
        scored = []
        for genome in population:
            model = DecisionModel(input_size, hidden_size, output_size)
            set_genome(model, genome)
            fitness = evaluate_fitness(model, data, labels)
            scored.append((fitness, genome))

        scored.sort(reverse=True)
        print(f"Gen {gen}: Best fitness {scored[0][0]:.3f}")

        # Selection
        top = [g for _, g in scored[:POP_SIZE // 5]]

        # Generate new population
        population = top[:]
        while len(population) < POP_SIZE:
            parent1, parent2 = random.sample(top, 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            population.append(child)

    return scored[0][1]  # Return best genome

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=200, n_features=4, n_classes=3, n_informative=4)
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.long)

genome = evolve(input_size=4, hidden_size=10, output_size=3, data=X, labels=y)
best_model = DecisionModel(4, 10, 3)
set_genome(best_model, genome)