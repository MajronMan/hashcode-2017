"""
Cellar Dwellers @ HashCode 2017
"""

from random import randint, random

retain_rate = 0
diversity_rate = 0
mutation_rate = 0
epochs_number = 0
population_size = 0

population = []


def evolve(population):
    graded = sorted([(c, rate_chromosome(c)) for c in population], key=lambda x: rate_chromosome(x),
                    reversed=True)
    retain_length = int(len(graded) * retain_rate)
    parents = graded[:retain_length]

    # diversity
    for chromosome in graded[retain_length:]:
        if random() < diversity_rate:
            parents.append(chromosome)

    # mutation
    for chromosome in parents:
        if random() < mutation_rate:
            mutate(chromosome)

    # breeding
    children_number = population_size - len(parents)
    children = []
    while len(children) < children_number:
        parent1 = randint(0, len(parents) - 1)
        parent2 = randint(0, len(parents) - 1)
        if parent1 != parent2:
            child = get_child(parent1, parent2)
            children.append(child)

    parents += children
    return parents


def mutate(chromosome):
    pass


def get_child(parent1, parent2):
    pass


def perform_epochs():
    pass


# temp
def rate_chromosome(chromosome):
    pass


# temp
def rate_population(population):
    pass


if __name__ == "__main__":
    perform_epochs()
