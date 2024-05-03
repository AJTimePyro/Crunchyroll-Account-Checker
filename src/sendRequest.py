#!/usr/bin/env python3


### Importing
from urllib import (
    request,
    parse,
    error
)
from http import client
import json


### Constants
DefaultHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}


### Request class
class Request:

    def __init__(
        self,
        url : str = str()
    ):

        self.url : str = url
        self.headers : dict = DefaultHeader
        self.payload : dict = dict()
        self.encodedPayload : bytes | None = None
        self.proxy : str = str()
    
    def setRequestData(
        self,
        url : str,
        headers : dict = dict(),
        payload : dict = dict(),
        proxy : str = str()
    ):
        self.setTargetUrl(url)
        self.updateHeader(headers)
        self.setProxy(proxy)

        if payload:
            self.bindPayloadData(payload)
    
    def sendRequest(self):
        self.__buildRequest()
        self.__openConnection()

    def sendRequestWithData(
        self,
        url : str,
        headers : dict = dict(),
        payload : dict = dict(),
        proxy : str = str()
    ):
        self.setRequestData(url, headers, payload, proxy)
        self.sendRequest()
    
    def setTargetUrl(
        self,
        url : str
    ):
        self.url = url
    
    def setProxy(
        self,
        proxy : str
    ):
        self.proxy = proxy
    
    def updateHeader(
        self,
        nHeaders : dict
    ):
        self.headers.update(nHeaders)
    
    def bindPayloadData(
        self,
        data : dict
    ):

        self.payload.update(data)
        self.encodedPayload = parse.urlencode(self.payload).encode()
    
    def _parseResponse(
        self,
        res
    ):
        res = res.read()
        res : str = res.decode('utf-8')
        if res.startswith("{"):
            res = json.loads(res)
        return res
    
    def __buildRequest(self):
        self.__req = request.Request(
            self.url,
            headers = self.headers,
            data = self.encodedPayload
        )

        if self.proxy:
            self.__req.set_proxy(self.proxy, 'http')
            self.__req.set_proxy(self.proxy, 'https')
    
    def __openConnection(self):
        errorLog : dict = {
            "errorType" : '',
            "error" : None
        }

        try:
            res = request.urlopen(self.__req, timeout = 5)
            
        except error.HTTPError as e:
            errorLog["error"] = e

            if e.code in (406, 429, 403):
                errorLog["errorType"] = "proxy"
            else:
                errorLog["errorType"] = "http"
            self.response = errorLog

        except (client.BadStatusLine, error.URLError) as e:
            errorLog["errorType"] = "proxy"
            errorLog["error"] = e
            self.response = errorLog

        except Exception as e:
            errorLog["errorType"] = "unkown"
            errorLog["error"] = e
            self.response = errorLog

        else:
            self.response = self._parseResponse(res)
    

    