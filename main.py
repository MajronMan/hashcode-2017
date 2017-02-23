"""
Cellar Dwellers @ HashCode 2017
"""

from random import randint, random

retain_rate = 0
diversity_rate = 0
mutation_rate = 0
epochs_number = 0
population_size = 0

best_chromosome = None
population = []


def evolve(population):
    global best_chromosome
    graded = sorted([c for c in population], key=lambda x: rate_chromosome(x),
                    reversed=True)
    best_chromosome = graded[0]
    retain_length = int(len(graded) * retain_rate)
    parents = graded[:retain_length]

    # diversity
    tmp = population_size - len(parents)
    for i in range(0, tmp):
        parents.append(get_random_gene())

    # breeding
    children_number = population_size - len(parents)
    children = []
    while len(children) < children_number:
        parent1 = randint(0, len(parents) - 1)
        parent2 = randint(0, len(parents) - 1)
        if parent1 != parent2:
            child1, child2 = get_children(parent1, parent2)
            children.append(child1)
            children.append(child2)

    parents += children
    return parents


def get_children(parent1, parent2):
    # TODO - get gene_number from Chromosome class?
    gene_number = 1
    split_point = randint(0, gene_number)
    child1 = Chromosome(parent1.cache_servers[:split_point] + parent2.cache_servers[split_point:])
    child2 = Chromosome(parent1.cache_servers[split_point:] + parent2.cache_servers[:split_point])
    mutate(child1)
    mutate(child2)
    return (child1, child2)


def mutate(chromosome):
    for i in range(len(chromosome.cache_servers)):
        if random() < mutation_rate:
            chromosome.cache_servers[i] = get_random_gene()
    pass


# --------- Todo --------
def get_random_chromosome():
    pass


def get_random_gene():
    pass


# --------- Todo --------


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
