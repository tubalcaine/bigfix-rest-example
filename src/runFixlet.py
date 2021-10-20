import argparse
import bigfixREST

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--bfserver", type=string, help="BigFix REST Server name/IP address")
parser.add_argument("-p", "--bfport", type=int, help="BigFix Port number (default 52311)", default=52311)
parser.add_argument("-U", "--bfuser", type=string, help="BigFix Console/REST User name")
parser.add_argument("-P", "--bfpass", type=string, help="BigFix Console/REST Password")
parser.add_argument("-m", "--match", type=string, help="Fixlet name pattern to match")
parser.parse_args()

bf = bigfixREST.bigfixRESTConnection(parser.bfserver, parser.bfport, parser.bfuser, parser.bfpass)

qres = bf.srQueryJson(f"(id of it, id of site of it | -1, content id of default action of it, concatenation \"~\" of names of applicable computers of it, name of it) of bes fixlets whose (exists applicable computer of it and exists default action of it and exists match (regex \"{parser.match}\") of name of it)")

print(qres)

for fixlet in qres["result"]:
    print(fixlet)
    s = ""
    tgtList = fixlet[4].split("~")
    bfar = bf.takeSourcedFixletAction(tgtList, fixlet[1], fixlet[0])
    print(bfar.getActionURL())

exit(0)