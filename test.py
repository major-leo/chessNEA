import json
from collections import defaultdict
dict = defaultdict(list)
try:
    file_handle = open('openingTable.txt','r+')
    dict = json.loads(file_handle.read())
except:
    pass
print(dict)
# json = json.dumps(dict)
# f = open("openingTable.txt","w")
# f.write(json)
# f.close()
