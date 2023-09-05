import sys
import json
from openpyxl import Workbook

inputfile = sys.argv[1]
outputfile = sys.argv[2]

book = Workbook()
sheet = book.active

sheet.append(("ip", "latency", "pver", "ver", "cplayers", "mplayers", "motd", "isicon"))

with open(inputfile) as f:
    data = json.load(f)
    for entry in data:
        sheet.append((entry["ip"], entry["latency"], entry["pver"], entry["ver"], entry["cplayers"], entry["mplayers"], entry["motd"], entry["isicon"]))

book.save(outputfile)