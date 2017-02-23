def perform_epochs():
    global videos, cache_servers, endpoints, population

    videos, cache_servers, endpoints, = read()
    population = get_initial_population()

    # log(i, population)
    for i in range(start=0, stop=None):
        population = evolve(population)
        save(best_chromosome)

        # if i % log_interval == 0:
        #     log(population)