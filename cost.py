def rate_chromosome(cacheservers):
    nom=0
    denom=0
    if len(requests)!=len(latencies):
        print("zjebaliście")
    for i in range(0, len(requests)):
        nom+=requests[i]*latencies[i]
        denom+=requests[1]
    return nom/denom
