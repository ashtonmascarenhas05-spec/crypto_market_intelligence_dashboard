import threading
import time

class ScraperEngine:
    def __init__(self,base_urls,headers,timeout,rate_limit):
        self.base_urls = base_urls
        self.headers = headers
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.results = []
        self.lock = threading.Lock()