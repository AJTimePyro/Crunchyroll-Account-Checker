#!/usr/bin/env python3


### Importing
from urllib import (
    request,
    parse,
    error
)
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
    
    def sendRequestWithData(
        self,
        url : str,
        headers : dict = dict(),
        payload : dict = dict()
    ):
        self.setTargetUrl(url)
        self.updateHeader(headers)
        self.bindPayloadData(payload)
        self.sendRequest()
    
    def sendRequest(self):
        self.__buildRequest()
        self.__openConnection()
    
    def setTargetUrl(
        self,
        url : str
    ):
        self.url = url
    
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
    
    def _parseResponse(
        self,
        res
    ):
        res = res.read()
        res = res.decode('utf-8')
        res = json.loads(res)
        return res
    
    def __buildRequest(self):
        self.__req = request.Request(
            self.url,
            headers = self.headers,
            data = self.payload
        )
    
    def __openConnection(self):
        errorLog : dict = {
            "errorType" : '',
            "error" : None
        }

        try:
            res = request.urlopen(self.__req)
            
        except error.HTTPError as e:
            errorLog["errorType"] = "http"
            errorLog["error"] = e
            self.response = errorLog

        except Exception as e:
            errorLog["errorType"] = "unkown"
            errorLog["error"] = e
            self.response = errorLog

        else:
            self.response = self._parseResponse(res)
    

    