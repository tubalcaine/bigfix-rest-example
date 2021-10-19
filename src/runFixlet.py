import argparse
import bigfixREST

bf = bigfixREST.bigfixRESTConnection("10.10.220.60", 52311, "IEMAdmin", "BigFix!123")

qres = bf.srQueryJson("(id of it, name of it, (id of it | -1, name of it | \"NA\") of site of it) of bes fixlets")

print(qres)

rows = bf.flattenQueryResult(qres)

print(rows)
