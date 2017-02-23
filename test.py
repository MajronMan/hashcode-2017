from data_types import *

i=Chromosome([])

i.to_file("kierwa")
i.cache_servers.append(CacheServer(2,[Video(2,1),Video(3,7)],2137))
i.to_file("kierwa")