class Video:
    def __init__(self, size, id):
        self.size = size
        self.id = id

class Endpoint:
    def __init__(self, links, id, requests):
        self.links = links
        self.id = id
        self.requests = requests

class Link:
    def __init__(self, latency, endpoint, cache_server):
        self.latency = latency
        self.endpoint = endpoint
        self.cache_server = cache_server

class CacheServer:
    def __init__(self, id, videos):
        self. id = id
        self.videos = videos

class Request:
    def __init__(self, video, endpoint, number):
        self.video = video
        self.endpoint = endpoint
        self.number = number