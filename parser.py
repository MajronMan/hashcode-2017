from data_types import *

class Parser:
    @staticmethod
    def read():
        v, e, r, c, x = list(map(int, input().split()))
        video_sizes = list(map(int, input().split())) # v numbers describing video sizes
        videos = [Video(video_sizes[i], i) for i in range(v)]
        cache_servers  =[CacheServer(i, {}, x) for i in range(c)]
        endpoints = []
        for i in range(e):
            ld, k = list(map(int, input().split())) # latency to datacenter and number of cache servers
            endpoints.append(Endpoint([], i, [], ld))
            for j in range(k):
                c, lc = list(map(int, input().split())) # id and latency to cache server
                endpoints[i].links.append(Link(lc, endpoints[i], cache_servers[c]))
        for i in range(r):
            rv, re, rn = list(map(int, input().split()))
            endpoints[re].requests.append(Request(videos[rv], endpoints[re], rn))
        return {'videos': videos, 'cache_servers': cache_servers, 'endpoints': endpoints}
