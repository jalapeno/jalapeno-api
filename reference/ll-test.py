import json
from arango import ArangoClient
from math import ceil

client = ArangoClient(hosts='http://198.18.133.111:30852')
db = client.db('jalapeno', username='root', password='jalapeno')
cursor = db.aql.execute("""for v, e in any shortest_path """ + '"gpus/host01-gpu01"' + """ \
    to """ + '"gpus/host12-gpu01"' + """ ipv6_graph options { weightAttribute: 'latency' } \
            return { node: v._key, name: v.name, sid: v.sids[0].srv6_sid, latency: e.latency } """)
path = [doc for doc in cursor]
# print("path: ", path)
hopcount = len(path)
#print("hops: ", hopcount)
pq = ceil((hopcount/2)-1)
#print(pq)
pq_node = (path[pq])
#print("pqnode: ", pq_node)
sid = 'sid'
usid_block = 'fc00:0:'
locators = [a_dict[sid] for a_dict in path]
for sid in list(locators):
    if sid == None:
        locators.remove(sid)
print("locators: ", locators)

usid = []
for s in locators:
    if s != None and usid_block in s:
        usid_list = s.split(usid_block)
        sid = usid_list[1]
        usid_int = sid.split(':')
        u = (usid_int[0])
        usid.append(u)

ipv6_separator = ":"

sidlist = ""
for word in usid:
    sidlist += str(word) + ":"
# print(sidlist)

srv6_sid = usid_block + sidlist + ipv6_separator
print("srv6 usid carrier: ", srv6_sid)

pathdict = {
        'source': 'gpus/host08-gpu02',
        'destination': 'gpus/host12-gpu02',
        'srv6 sid list': locators,
        'srv6 usid': srv6_sid,
    }
    
pathobj = json.dumps(pathdict, indent=4)
# return(pathobj)
print(pathobj)