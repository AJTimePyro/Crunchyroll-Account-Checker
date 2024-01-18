#!/usr/bin/env python3


### Importing
from src import sendRequest


### Proxy Class
class Proxy:

    def __init__(self):
        self.proxy_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        self.request = sendRequest.Request()
        self.filepath = "resources/proxy.txt"

    def getProxies(self):
        self.request.sendRequestWithData(self.proxy_api_url)
        self.writeToFile()
    
    def writeToFile(self):
        with open(self.filepath, 'w') as file:
            file.write(self.request.response)

