import argparse
import bigfixREST

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--bfserver", type=str, help="BigFix REST Server name/IP address")
parser.add_argument("-p", "--bfport", type=int, help="BigFix Port number (default 52311)", default=52311)
parser.add_argument("-U", "--bfuser", type=str, help="BigFix Console/REST User name")
parser.add_argument("-P", "--bfpass", type=str, help="BigFix Console/REST Password")
parser.add_argument("-m", "--match", type=str, help="Fixlet name pattern to match")
conf = parser.parse_args()

bf = bigfixREST.bigfixRESTConnection(conf.bfserver, conf.bfport, conf.bfuser, conf.bfpass)

query = f'''
(id of it, id of site of it | -1, 
content id of default action of it, 
concatenation \"|\" of names of applicable computers of it, 
name of it) 
 of bes fixlets whose (exists applicable computer of it and 
 exists default action of it and 
 exists match (regex \"{conf.match}\") of name of it)'''.strip()

qres = bf.srQueryJson(query)

print(qres)

for fixlet in qres["result"]:
    print(fixlet)
    tgtList = fixlet[3].split("|")
    bfar = bf.takeSourcedFixletAction(tgtList, fixlet[1], fixlet[0])
    print(bfar.getActionResultXML)
    print(bfar.getActionURL())
    print(bfar.getActionID)

exit(0)
