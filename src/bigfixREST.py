import requests
import json
import xml.etree.ElementTree as ET

# This is here ONLY to suppress self-signed certoficate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# End of warning supression


## bigFixActionResult class
class bigfixActionResult():

    def __init__(self, resxml):
        self.xml = resxml
        self.root = ET.fromstring(resxml)

    def getActionID(self):
        thing = self.root.findall("Action/ID")
        id = thing[0].text
        return id


    def getActionURL(self):
        thing = self.root.findall("Action")
        attrs = thing[0].attrib
        return attrs["Resource"]


    def getActionResultXML(self):
        return self.xml



## bigfixRESTConnection class
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

        templ = templ.replace("__SiteID__", str(siteId))
        templ = templ.replace("__FixletID__", str(fixletId))
        templ = templ.replace("__ActionID__", actionId)
        templ = templ.replace("__Title__", title)

        targets = ""
        for tgt in targetList:
            targets += "<ComputerName>" + tgt + "</ComputerName>\n"

        templ = templ.replace("__TargetList__", targets)
        
        qheader = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        req = requests.Request('POST'
            , self.url + "/api/actions"
            , headers=qheader
            , data=templ
        )

        prepped = self.sess.prepare_request(req)
            
        result = self.sess.send(prepped, verify = False)

        if (result.status_code == 200):
            print(result)
            return bigfixActionResult(result.content)
        else:
            return None

