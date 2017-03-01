"""
Cellar Dwellers @ HashCode 2017
"""


class Video:
    def __init__(self, size, id):
        self.size = size
        self.id = id

    def __str__(self):
        return "id: " + str(self.id) + " size: " + str(self.size)

    def __repr__(self):
        return self.__str__()


class Endpoint:
    def __init__(self, links, id, requests, data_center_latency):
        self.links = links
        self.id = id
        self.requests = requests
        self.data_center_latency = data_center_latency

    def __str__(self):
        return "\nid:" + str(self.id) + "\n" + \
               "\n".join(map(str, [str(link) for link in self.links])) + "\n" + \
               "\n".join(map(str, [str(link) for link in self.requests]))

    def __repr__(self):
        return self.__str__()


class Link:
    def __init__(self, latency, endpoint_id, cache_server_id):
        self.latency = latency
        self.endpoint_id = endpoint_id
        self.cache_server_id = cache_server_id

    def __str__(self):
        return str(self.cache_server_id) + " --" + str(self.latency) + "-->" + str(self.endpoint_id)

    def __repr__(self):
        return self.__str__()


class CacheServer:
    def __init__(self, id, videos, size):
        self.id = id
        self.videos = set(videos)
        self.size = size

    def __str__(self):
        return "\nid: " + str(self.id) + " size: " + str(self.size) + '\n' + \
               "\n".join(list(map(str, self.videos)))

    def __repr__(self):
        return self.__str__()


class Request:
    def __init__(self, video, endpoint, number):
        self.video = video
        self.endpoint = endpoint
        self.number = number

    def available_links(self, cache_servers):
        result = []
        for link in self.endpoint.links:
            if self.video in cache_servers[link.cache_server_id].videos:
                result.append(link)
        return result

    def __str__(self):
        return "video " + str(self.video.id) + "--> " + str(self.endpoint.id) + " x" + str(self.number)

    def __repr__(self):
        return self.__str__()


class Chromosome:
    def __init__(self, cache_servers):
        self.cache_servers = cache_servers

    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.truncate()
            f.write(str(len(self.cache_servers)) + '\n')
            for i in range(0, len(self.cache_servers)):
                server = self.cache_servers[i]
                f.write(str(i) + " ")
                for video in server.videos:
                    f.write(str(video.id) + " ")
                f.write('\n')

    def __str__(self):
        return "\n".join(list(map(str, self.cache_servers)))

    def __repr__(self):
        return self.__str__()


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
