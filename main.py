"""
Cellar Dwellers @ HashCode 2017
"""

from random import randint, random

retain_rate = 0
diversity_rate = 0
mutation_rate = 0
epochs_number = 0
population_size = 0
cache_servers_number = 0

videos = []
cache_servers = []

endpoints = []

best_chromosome = None
best_chromosome_score = None
population = []


class Video:
    def __init__(self, size, id):
        self.size = size
        self.id = id

    def __str__(self):
        return "id: " + str(self.id) + " size: " + str(self.size)

    def __repr__(self):
        return self.__str__()


class Endpoint:
    def __init__(self, links, id, requests, data_center_latency):
        self.links = links
        self.id = id
        self.requests = requests
        self.data_center_latency = data_center_latency

    def __str__(self):
        return "\nid:" + str(self.id) + "\n" + \
               "\n".join(map(str, [str(link) for link in self.links])) + "\n" + \
               "\n".join(map(str, [str(link) for link in self.requests]))

    def __repr__(self):
        return self.__str__()


class Link:
    def __init__(self, latency, endpoint, cache_server):
        self.latency = latency
        self.endpoint = endpoint
        self.cache_server = cache_server

    def __str__(self):
        return str(self.cache_server.id) + " --" + str(self.latency) + "-->" + str(self.endpoint.id)

    def __repr__(self):
        return self.__str__()


class CacheServer:
    def __init__(self, id, videos, size):
        self.id = id
        self.videos = videos
        self.size = size

    def __str__(self):
        return "id: " + str(self.id) + " size: " + str(self.size)

    def __repr__(self):
        return self.__str__()


class Request:
    def __init__(self, video, endpoint, number):
        self.video = video
        self.endpoint = endpoint
        self.number = number

        def available_links():
            result = []
            for link in endpoint.links:
                if video in link.cache_server.videos:
                    result.append(link)
            return result

    def __str__(self):
        return "video " + str(self.video.id) + "--> " + str(self.endpoint.id) + " x" + str(self.number)

    def __repr__(self):
        return self.__str__()


class Chromosome:
    def __init__(self, cache_servers):
        self.cache_servers = cache_servers

    def to_file(self, filename):
        f = open(filename, 'w')
        f.truncate()
        f.write(str(len(self.cache_servers)) + '\n')
        for i in range(0, len(self.cache_servers)):
            server = self.cache_servers[i]
            f.write(str(i) + " ")
            for video in server.videos:
                f.write(str(video.id) + " ")
        f.write('\n')


def read():
    v, e, r, c, x = list(map(int, input().split()))
    video_sizes = list(map(int, input().split()))  # v numbers describing video sizes
    videos = [Video(video_sizes[i], i) for i in range(v)]
    cache_servers = [CacheServer(i, [], x) for i in range(c)]
    datacenter = CacheServer(-1, [], -1)
    endpoints = []
    for i in range(e):
        endpoints.append(Endpoint([], i, []))
        ld, k = list(map(int, input().split()))  # latency to datacenter and number of cache servers
        # id of datacenter is -1
        endpoints[i].links.append(Link(ld, endpoints[i], datacenter))
        for j in range(k):
            c, lc = list(map(int, input().split()))  # id and latency to cache server
            endpoints[i].links.append(Link(lc, endpoints[i], cache_servers[c]))
    for i in range(r):
        rv, re, rn = list(map(int, input().split()))
        endpoints[re].requests.append(Request(videos[rv], endpoints[re], rn))
    return {'videos': videos, 'cache_servers': cache_servers, 'endpoints': endpoints}


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
        parents.append(get_random_chromosome())

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
    split_point = randint(0, cache_servers_number)
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
    for i in range(cache_servers_number):
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
        population.append(get_random_chromosome())

    return initial_population


def log(i, population):
    pass


def perform_epochs():
    global videos, cache_servers, endpoints, population

    videos, cache_servers, endpoints, = read()
    population = get_initial_population()

    # log(i, population)
    for i in range(start=0, stop=None):
        population = evolve(population)
        best_chromosome.to_file("best.out")

        # if i % log_interval == 0:
        #     log(population)


def rate_chromosome():
    global endpoints

    nom = 0
    denom = 0
    for endpoint in endpoints:
        for request in endpoint.requests:
            best_latency = endpoint.data_center_latency
            for link in request.available_links():
                if link.latency < best_latency:
                    best_latency = link.latency
            nom += request.number * best_latency
            denom += request.number
    return nom / denom


def rate_population(population):
    pass


if __name__ == "__main__":
    pass
