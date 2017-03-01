"""
Cellar Dwellers @ HashCode 2017
"""

import math
from random import randint, random, choice

from data_types import *

retain_rate = 0.9
diversity_rate = 0.2
crossover_rate = 1.0
mutation_rate = 0.1
epochs_number = int(1e5)
population_size = 500
epoch_step = 500

saturation_mutation_rate_delta = 0.02
saturation_retain_rate_delta = -0.05
saturation_max_epochs = 1000

videos = []
cache_servers = []
endpoints = []
population = []

best_chromosome = None
best_chromosome_score = 0.0

current_mutation_rate = mutation_rate
current_retain_rate = retain_rate
saturation_epochs_count = 0

epoch_nr = 0


def evolve(epoch_population):
    global best_chromosome, epoch_nr, best_chromosome_score, saturation_max_epochs, saturation_epochs_count, \
        mutation_rate, current_mutation_rate

    epoch_nr += 1

    graded = [(c, rate_chromosome(c)) if c.score == 0 else (c, c.score) for c in epoch_population]
    graded = [x[0] for x in sorted(graded, key=lambda x: x[1], reverse=True)]

    best_chromosome = graded[0]
    score = rate_chromosome(best_chromosome)

    # saturation
    if math.isclose(score, best_chromosome_score):
        saturation_epochs_count += 1

        if saturation_epochs_count == saturation_max_epochs:
            desaturate()
            saturation_epochs_count = 0
    else:
        saturation_epochs_count = 0

    if score > best_chromosome_score:
        best_chromosome_score = score
        log_epoch(epoch_nr, score)
        best_chromosome.to_file("./results/" + str(score) + "best.out")

    elif epoch_nr % epoch_step == 0:
        log_epoch(epoch_nr, score)
    retain_length = int(len(graded) * current_retain_rate)
    parents = graded[:retain_length]

    # diversity
    for chromosome in graded[retain_length:]:
        if random() < diversity_rate and len(parents) < population_size:
            parents.append(chromosome)

    # breeding
    children_number = population_size - len(parents)
    children = []
    while len(children) < children_number:
        mother = roulette_choice(parents, parents[0].score)
        father = roulette_choice(parents, parents[0].score)
        if mother != father:
            child1, child2 = get_children(mother, father)
            children.append(child1)
            children.append(child2)

    parents += children
    return parents


def log_epoch(epoch_nr, score):
    print("Epoch\t{:6d}\t\tscore\t{:.6f}".format(epoch_nr, score))


def desaturate():
    global current_mutation_rate, current_retain_rate

    current_mutation_rate += saturation_mutation_rate_delta
    current_retain_rate += saturation_retain_rate_delta

    print("Saturation: epoch {}\tmutation: {:.4f}\tretain: {:.4f}".format(epoch_nr, current_mutation_rate,
                                                                          current_retain_rate))


def roulette_choice(population, max_score):
    candidate = None
    accepted = False

    while not accepted:
        candidate = choice(population)
        if random() < candidate.score / max_score:
            accepted = True

    return candidate


def get_children(parent1, parent2):
    split_point = randint(0, len(cache_servers)) if random() < crossover_rate else len(cache_servers)

    child1 = Chromosome(parent1.cache_servers[:split_point] + parent2.cache_servers[split_point:])
    child2 = Chromosome(parent1.cache_servers[split_point:] + parent2.cache_servers[:split_point])
    mutate(child1)
    mutate(child2)
    return child1, child2


def mutate(chromosome):
    for i in range(len(chromosome.cache_servers)):
        if random() < current_mutation_rate:
            server = chromosome.cache_servers[i]
            chromosome.cache_servers[i] = get_random_gene(server.id, server.size)


def get_random_chromosome():
    chromosome = Chromosome([])
    for i in range(len(cache_servers)):
        size = cache_servers[i].size
        id = cache_servers[i].id
        chromosome.cache_servers.append(get_random_gene(id, size))
    return chromosome


def get_random_gene(server_id, size):
    server = CacheServer(server_id, [], size)
    loaded_size = 0
    while True:
        video = videos[randint(0, len(videos) - 1)]
        if loaded_size + video.size <= server.size and video not in server.videos:
            server.videos.add(video)
            loaded_size += video.size
        else:
            break
    return server


def get_initial_population():
    initial_population = []

    for i in range(population_size):
        initial_population.append(get_random_chromosome())

    return initial_population


def rate_chromosome(chromosome):
    nom = 0
    denom = 0
    for endpoint in endpoints:
        for request in endpoint.requests:
            best_latency = endpoint.data_center_latency
            for link in request.available_links(chromosome.cache_servers):
                if link.latency < best_latency:
                    best_latency = link.latency
            nom += request.number * (endpoint.data_center_latency - best_latency)
            denom += request.number
    chromosome.score = nom / denom
    return chromosome.score


def perform_epochs():
    global videos, cache_servers, endpoints, population
    p = Parser.read_from_file('me_at_the_zoo.in')
    videos = p['videos']
    cache_servers = p['cache_servers']
    endpoints = p['endpoints']
    print("File parsed")
    population = get_initial_population()
    print("Initial population constructed")

    for i in range(0, epochs_number):
        population = evolve(population)


if __name__ == "__main__":
    perform_epochs()
