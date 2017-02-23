def cost(requests, latencies):
    nom=0;
    denom=0;
    for i in range(0, len(requests)):
        nom+=requests[i]*latencies[i]
        denom+=requests[1]
    return nom/denom
