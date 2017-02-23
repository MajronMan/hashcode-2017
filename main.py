"""
Cellar Dwellers @ HashCode 2017
"""

from random import randint, random

retain = 0
diversity_rate = 0
mutation = 0
epochs_number = 0

population = []


def evolve(population):
    graded = sorted([(c, rate_chromosome(c)) for c in population], key=lambda x: rate_chromosome(x),
                    reversed=True)
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # diversity
    for chromosome in graded[retain_length:]:
        if random() > diversity_rate:
            parents.append(chromosome)

    # mutation
    for chromosome in parents:
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