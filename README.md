# pymcstatus
A python script to sort through a list of ip's to find working minecraft servers   
   
Usage:   
```
Usage:
srvstatus.py -p IP
srvstatus.py -f inlist.txt
srvstatus.py -f inlist.txt -o outfile.json
```

Then convert json to xlsx using: 
```
json2xlsx.py infile.json outfile.xlsx
```

Dependencies:
```
Pillow mcstatus openpyxl
```