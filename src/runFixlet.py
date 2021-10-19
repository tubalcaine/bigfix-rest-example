import argparse
import bigfixREST

bf = bigfixREST.bigfixRESTConnection("10.10.220.60", 52311, "IEMAdmin", "BigFix!123")

qres = bf.srQueryJson("(id of it, id of site of it | -1, content id of default action of it, name of it) of bes fixlets whose (exists applicable computer of it and exists default action of it and exists match (regex \"[Ff]irefox\") of name of it)")

print(qres)

