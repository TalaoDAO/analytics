import http.client
from datetime import datetime
import json



def getOperationStatus(hash):

    conn = http.client.HTTPSConnection("api.ithacanet.tzkt.io")
    headers = {
        }
  
    link="/v1/operations/"+hash 
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonExample=json.loads(output)


    #print(result)
    print("here"+str(len(jsonExample)))
    with open('json_data.json', 'w') as mon_fichier:
        json.dump(jsonExample, mon_fichier)
    try:
        return jsonExample[0]["status"]
    except KeyError:
        return None
    except IndexError:
        return None

def getOperationAmount(hash):

    conn = http.client.HTTPSConnection("api.ithacanet.tzkt.io")
    headers = {
        }
  
    link="/v1/operations/"+hash 
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonExample=json.loads(output)


    #print(result)
    print("here"+str(len(jsonExample)))
    with open('json_data.json', 'w') as mon_fichier:
        json.dump(jsonExample, mon_fichier)
    return jsonExample[0]["amount"]
#print(getOperationStatus("ooMLWbsuzYkBSdGkiA249Fk19WrMFUjY94yKAR717HNZiZffEjh"))