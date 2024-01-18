#!/usr/bin/env python3


### Importing
from src import sendRequest


### Proxy Class
class Proxy:

    def __init__(self):
        self.proxy_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        self.request = sendRequest.Request()
        self.filepath = "resources/proxy.txt"
        self.proxies : tuple[str] = tuple()
        self.proxyIndex = 0

    def getProxies(self):
        self.request.sendRequestWithData(self.proxy_api_url)
        self.writeToFile()
    
    def writeToFile(self):
        with open(self.filepath, 'w') as file:
            file.write(self.request.response)
        self.openFile()
    
    def openFile(self):
        self._file = open(self.filepath)
        self.parseProxies()
    
    def parseProxies(self):
        self.proxies = tuple(map(
            lambda x: x.removesuffix('\n'),
            self._file.readlines())
        )
    
    def getProxy(self):
        if len(self.proxies) == 0:
            return str()
        
        if self.proxyIndex >= len(self.proxies):
            self.proxyIndex = 0
        return self.proxies[self.proxyIndex]
    
    def nextIndex(self):
        if self.proxyIndex == len(self.proxies) - 1:
            self.proxyIndex = 0
        else:
            self.proxyIndex += 1

