import http.client
from datetime import datetime
import json



def getOperationAmount(hash):

    conn = http.client.HTTPSConnection("api.hangzhou2net.tzkt.io")
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
#print(getOperationAmount("opJsMk6gTztj2YNyx479Fjd1dLEytVLohhiBQuRykUSiPAvWMFn"))