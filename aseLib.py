from Common.commonLib import CommonLib
import requests

class ASELib(CommonLib):

    # autorization info exists after authorizing to ASE
    authInfo = {}
    authHeaders = {}
    authCookies = {}

    # process the command-line options and performs the initial authorization with ASE
    def __init__(self):
        super().__init__()
        if not "host" in self.Options: raise AssertionError("Options[\"host\"] is missing - ASE options must contain the ASE server host name")
        self.authorize()

    def host(self):
        return self.Options["host"]

    def authorize(self, Id=None, Secret=None, asUNPW=False):
        if (Id == None):
            if (not self.Options):
                self.getCommandLineOptions()
            # if we have a KeyId and it's not empty, we prefer the ID/Secret combination
            if ("KeyId" in self.Options["ase"] and self.Options["ase"]["KeyId"]):
                Id = self.Options["ase"]["KeyId"]
                Secret = self.Options["ase"]["KeySecret"]
            else:
                Id = self.Options["ase"]["Username"]
                Secret = self.Options["ase"]["Password"]
                asUNPW = True
        
        if (asUNPW):
            loginObj = {"userId": Id, "password": Secret, "featureKey": "AppScanEnterpriseUser"}
            res = requests.post(f"{self.host()}/ase/api/login", json=loginObj, verify=False)
            self.authInfo = res.json()
        else:
            loginObj = {"keyId": Id, "keySecret": Secret}
            res = requests.post(f"{self.host()}/ase/api/eylogin/apikeylogin", json=loginObj, verify=False)
            self.authInfo = res.json()

        if (res.status_code != 200):
            print(res.text)
            return

        self.authHeaders = {"asc_xsrf_token":self.authInfo["sessionId"]}
        self.authCookies = res.cookies
        
    # performs a GET operation, authorizing if needed
    # URI is the relative call - the host is added automatically
    def get(self, uri, **kwargs):
        if (not self.authInfo):
            self.authorize()

        self.prepareRequest(kwargs)

        uri = self.host() + uri

        res = requests.get(uri,**kwargs)
        if (res.status_code == 401):
            self.authorize()
            self.addAuthHeaders(kwargs)
            self.addAuthCookies(kwargs)
            res = requests.get(uri, **kwargs)

        if (res.status_code != 200):
            print(res.text)

        return res

    # performs a POST operation, authorizing if needed
    # URI is the relative call - the host is added automatically
    def post(self, uri, **kwargs):
        if (not self.authInfo):
            self.authorize()

        self.prepareRequest(kwargs)

        uri = self.host() + uri

        res = requests.post(uri, **kwargs)
        if (res.status_code == 401):
            self.authorize()
            self.addAuthHeaders(kwargs)
            self.addAuthCookies(kwargs)
            res = requests.get(uri, **kwargs)

        if (res.status_code != 200):
            print(res.text)

        return res


    def prepareRequest(self, reqArgs):
        self.addAuthHeaders(reqArgs)
        self.addAuthCookies(reqArgs)
        # if working with a self-signed instance, ignore certificate errors
        reqArgs["verify"] = False

    # adds the authorization header to the request. If a "headers" key exists in the request object, the auth headers
    # are added. If "headers" do not exist the auth headers are set with "headers" key
    def addAuthHeaders(self, reqArgs):
        if ("headers" in reqArgs):
            reqArgs["headers"].update(self.authHeaders)
        else:
            reqArgs["headers"] = self.authHeaders

    # adds the session ID cookie to the request. If a "cookies" key exists in the request object, the cookie
    # is added. If "cookies" do not exist the cookie is set with the "cookies" ket
    def addAuthCookies(self, reqArgs):
        if ("cookies" in reqArgs):
            reqArgs["cookies"].update(self.authCookies)
        else:
            reqArgs["cookies"] = self.authCookies