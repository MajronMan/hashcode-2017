from parser import Parser


def log(i, population):
    print("--------------------\nEpoch "+ i, "\n".join(list(map(str, population))))

log_interval = 1

def perform_epochs():
    global videos, cache_servers, endpoints, population

    videos, cache_servers, endpoints, = Parser.read()
    population = get_initial_population()

    # log(i, population)
    for i in range(start=0, stop=None):
        population = evolve(population)
        save(best_chromosome)

        # if i % log_interval == 0:
        #     log(population)