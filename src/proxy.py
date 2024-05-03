#!/usr/bin/env python3


### Importing
from src import sendRequest
from typing import Union


### Constant
DEFAULT_FILEPATH = "resources/proxy.txt"


### Proxy Class
class Proxy:

    def __init__(
        self,
        proxy_filename : Union[str, None] = None,
        proxyEnable : bool = False
        ):
        self.proxy_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        self.proxies : list[str] = list()
        self.proxyIndex = 0
        self.proxyEnable = proxyEnable

        if self.proxyEnable:
            if proxy_filename:
                self.filepath = proxy_filename
                self.openFile()
            else:
                self.filepath = DEFAULT_FILEPATH
                self.getProxies()

    def getProxies(self):
        request = sendRequest.Request()
        request.sendRequestWithData(self.proxy_api_url)
        self.writeToFile(str(request.response))
    
    def writeToFile(
        self,
        res : str
    ):
        with open(self.filepath, 'w') as file:
            file.write(res)
        self.openFile()
    
    def openFile(self):
        self._file = open(self.filepath)
        self.parseProxies()
    
    def parseProxies(self):
        self.proxies = list(map(
            lambda x: x.removesuffix('\n'),
            self._file.readlines())
        )
    
    def getProxy(self):
        if len(self.proxies) == 0:
            return str()
        return self.proxies[self.proxyIndex]
    
    def nextIndex(self):
        if self.proxyEnable == False:
            return
        if self.proxyIndex == len(self.proxies) - 1:
            self.proxyIndex = -1
        self.proxyIndex += 1
