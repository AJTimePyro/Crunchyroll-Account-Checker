#!/usr/bin/env python3


### Importing
from urllib import request, parse


class CrunchyrollChecker:

    def __init__(self):
        self.apiUrl = "https://beta-api.crunchyroll.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.auth = "Basic aHJobzlxM2F3dnNrMjJ1LXRzNWE6cHROOURteXRBU2Z6QjZvbXVsSzh6cUxzYTczVE1TY1k="
        self.data = {
            "grant_type": "password",
            "scope": "offline_access"
        }
    
    def _makeRequest(
        self,
        url : str,
        headers : dict = None,
        data : dict = None,
        param = None
        ):
        data = parse.urlencode(data).encode()
        req = request.Request(
            url,
            headers = headers,
            data = data,
            param = param
        )
        self.res = request.urlopen(req)

        self.res = self.res.read()
        self.res = self.res.decode('utf-8')
        self.res = dict(self.res)
        print(self.res)
    
    def _tryToLogin(
        self,
        email : str,
        password : str
        ):
        data = dict(self.data)
        data['username'] = email
        data['password'] = password
        headers = dict(self.headers)
        headers["authorization"] = self.auth
        self._makeRequest(
            self.apiUrl + "auth/v1/token",
            headers,
            data
        )
    
    def checker(self):
        self._tryToLogin

