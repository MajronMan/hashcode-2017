from data_types import *
from main import get_initial_population


pop=get_initial_population()
print(pop)
chr=pop[0]
for ch in pop:
    print(ch.cache_servers)

chr.to_file("test")