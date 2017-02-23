from data_types import *

class Parser:
    @staticmethod
    def read():
        return Parser._read(input)
    @staticmethod
    def _read(inputMethod):
        v, e, r, c, x = list(map(int, inputMethod().split()))
        video_sizes = list(map(int, inputMethod().split()))  # v numbers describing video sizes
        videos = [Video(video_sizes[i], i) for i in range(v)]
        cache_servers = [CacheServer(i, {}, x) for i in range(c)]
        endpoints = []
        for i in range(e):
            ld, k = list(map(int, inputMethod().split()))  # latency to datacenter and number of cache servers
            endpoints.append(Endpoint([], i, [], ld))
            for j in range(k):
                c, lc = list(map(int, inputMethod().split()))  # id and latency to cache server
                endpoints[i].links.append(Link(lc, i, c))
        for i in range(r):
            rv, re, rn = list(map(int, inputMethod().split()))
            endpoints[re].requests.append(Request(videos[rv], endpoints[re], rn))
        return {'videos': videos, 'cache_servers': cache_servers, 'endpoints': endpoints}

    @staticmethod
    def read_from_file(filename):
        f = open(filename, 'r')
        return Parser._read(f.readline)
