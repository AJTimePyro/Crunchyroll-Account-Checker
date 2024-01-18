#!/usr/bin/env python3


### Importing
from src import sendRequest


### Proxy Class
class Proxy:

    def __init__(self):
        self.proxy_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        self.request = sendRequest.Request()

    def getProxies(self):
        self.request.sendRequestWithData(self.proxy_api_url)
        print(self.request.response)

