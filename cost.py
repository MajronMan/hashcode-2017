def rate_chromosome(endpoints):
    nom=0
    denom=0
    for endpoint in endpoints:
        for request in endpoint.requests:
            best_latency=endpoint.data_center_latency
            for link in request.available_links():
                if link.latency<best_latency:
                    best_latency=link.latency
            nom+=request.number*best_latency
            denom+=request.number
    return nom/denom
