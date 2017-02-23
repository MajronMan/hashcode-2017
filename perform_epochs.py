def perform_epochs:
    population = get_initial_population()

    log(population)
    for i in range(start=0, stop=None):
        population = evolve(population)
        save(best)

        if i % log_interval == 0:
            log(population)
