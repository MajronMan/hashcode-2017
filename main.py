"""
Cellar Dwellers @ HashCode 2017
"""

from random import randint, random
from data_types import *

retain_rate = 0.5
diversity_rate = 0.2
mutation_rate = 0.25
epochs_number = int(1e5)
population_size = 8
epoch_step = 500

videos = []
cache_servers = []
endpoints = []
population = []

best_chromosome = None
best_chromosome_score = 0.0

epoch_nr = 0


def evolve(epoch_population):
    global best_chromosome, epoch_nr, best_chromosome_score
    epoch_nr += 1
    graded = sorted([c for c in epoch_population], key=lambda x: rate_chromosome(x),
                    reverse=True)
    best_chromosome = graded[0]
    score = rate_chromosome(best_chromosome)
    if score > best_chromosome_score:
        best_chromosome_score = score
        print("Progress: Best score in epoch {} is {}".format(epoch_nr, score))
        best_chromosome.to_file("./results/" + str(score) + "best.out")
    elif epoch_nr % epoch_step == 0:
        print("Epoch {}, best score {}".format(epoch_nr, score))
    retain_length = int(len(graded) * retain_rate)
    parents = graded[:retain_length]

    # diversity
    for chromosome in graded[retain_length:]:
        if random() < diversity_rate and len(parents) < population_size:
            parents.append(chromosome)

    # breeding
    children_number = population_size - len(parents)
    children = []
    while len(children) < children_number:
        parent1 = parents[randint(0, len(parents) - 1)]
        parent2 = parents[randint(0, len(parents) - 1)]
        if parent1 != parent2:
            child1, child2 = get_children(parent1, parent2)
            children.append(child1)
            children.append(child2)

    parents += children
    return parents


def get_children(parent1, parent2):
    split_point = randint(0, len(cache_servers))
    child1 = Chromosome(parent1.cache_servers[:split_point] + parent2.cache_servers[split_point:])
    child2 = Chromosome(parent1.cache_servers[split_point:] + parent2.cache_servers[:split_point])
    mutate(child1)
    mutate(child2)
    return child1, child2


def mutate(chromosome):
    for i in range(len(chromosome.cache_servers)):
        if random() < mutation_rate:
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
            server.videos.append(video)
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
    return nom / denom


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
