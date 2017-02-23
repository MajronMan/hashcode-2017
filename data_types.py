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
    def __init__(self, latency, endpoint, cache_server):
        self.latency = latency
        self.endpoint = endpoint
        self.cache_server = cache_server

    def __str__(self):
        return str(self.cache_server.id) + " --" + str(self.latency) + "-->" + str(self.endpoint.id)

    def __repr__(self):
        return self.__str__()


class CacheServer:
    def __init__(self, id, videos, size):
        self.id = id
        self.videos = videos
        self.size = size

    def __str__(self):
        return "id: " + str(self.id) + " size: " + str(self.size)

    def __repr__(self):
        return self.__str__()


class Request:
    def __init__(self, video, endpoint, number):
        self.video = video
        self.endpoint = endpoint
        self.number = number

        def available_links():
            result = []
            for link in endpoint.links:
                if video in link.cache_server.videos:
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
        f = open(filename, 'w')
        f.truncate()
        f.write(str(len(self.cache_servers)) + '\n')
        for i in range(0, len(self.cache_servers)):
            server = self.cache_servers[i]
            f.write(str(i) + " ")
            for video in server.videos:
                f.write(str(video.id) + " ")
        f.write('\n')
