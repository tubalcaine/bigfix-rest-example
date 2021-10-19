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

    # The idea of this stub method is that we can parse up the return tuple, mangling the
    # relevance property names to single tokens, and then returning an array of dictionaries,
    # each row of which contains a "row" entry with a flat array and a "dict" entry with
    # the mangled names and values. Usually when you write a relevance query, you know what the
    # positions are in absolute terms. I haven't decided if this is a good idea...
#    def flattenQueryResult(self, qres):
#        return None

    def takeSourcedFixletAction(self, targetList, siteId, fixletId, actionId = "Action1", title = "Programmatic Action from Python Script"):
        templ = '''\
<?xml version="1.0" encoding="UTF-8" ?>
<BES xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" >
<SourcedFixletAction>
	<SourceFixlet>
		<SiteID>__SiteID__</SiteID>
		<FixletID>__FixletID__</FixletID>
		<Action>__ActionID__</Action>
	</SourceFixlet>
	<Target>
        __TargetList__
	</Target>
	<Settings>
	</Settings>
	<Title>__Title__</Title>
</SourcedFixletAction>
</BES>
'''.strip()

        templ.replace("__SiteID__", siteId)
        templ.replace("__FixletID__", fixletId)
        templ.replace("__ActionID__", actionId)
        templ.replace("__Title__", title)

