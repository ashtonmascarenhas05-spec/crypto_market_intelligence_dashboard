import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor

class ScraperEngine:
    def __init__(self,base_urls,headers,timeout,rate_limit,expected_keys):
        self.base_urls = base_urls
        self.headers = headers
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.expected_keys = expected_keys
        self.results = []
        self.lock = threading.Lock()

    def fetch_single(self, url):
        ### fetch api data from url(json)
        try:    
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                if self.validate_data(data):
                    with self.lock:
                        self.results.append(data)
                time.sleep(self.rate_limit)  # Simulate rate limiting
                return f"Fetched data from {url}"
            else:
                return f"Failed to fetch data from {url}: Status code {response.status_code}"
        except Exception as e:
            return f"Error fetching data from {url}: {str(e)}"
        
    def fetch_all(self):
        with ThreadPoolExecutor(max_workers= 1) as executor:
            status_messages = list(executor.map(self.fetch_single, self.base_urls))
            for message in status_messages:
                print(message)
        return list(self.results)

    ##checks if the returned data has the expected keys.
    def validate_data(self, data):  # Example expected keys
        for key in self.expected_keys:
            if key not in data:
                return False
        return True    