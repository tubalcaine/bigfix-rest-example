import requests
import json

# This is here ONLY to suppress self-signed certoficate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# End of warning supression


class bigfixRESTConnection():

    def __init__(self, bfserver, bfport, bfuser, bfpass):
        self.bfserver = bfserver
        self.bfport = bfport
        self.bfuser = bfuser
        self.bfpass = bfpass
        self.sess = requests.Session()
        self.url = "https://"  + self.bfserver + ":" + str(self.bfport) 

        self.sess.auth = (self.bfuser, self.bfpass)
        resp = self.sess.get(self.url + "/api/login", verify=False)

    def srQueryJson(self, srquery):
        qheader = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        qquery = {
            "relevance" : srquery,
            "output"    : "json"
        }
        
        req = requests.Request('POST'
            , self.url + "/api/query"
            , headers=qheader
            , data=qquery
            )
            
        prepped = self.sess.prepare_request(req)
        result = self.sess.send(prepped, verify = False)
        
        if (result.status_code == 200):
            rv = json.loads(result.text)
            rv["query"] = srquery
            return rv

        return None

    def flattenQueryResult(self, qres):
        return None
