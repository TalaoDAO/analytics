import http.client
from datetime import datetime
import json
import sys


def getOperationStatus(hash):

    conn = http.client.HTTPSConnection("api.ghostnet.tzkt.io")
    headers = {
        }
  
    link="/v1/operations/"+hash 
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonExample=json.loads(output)
    try:
        return jsonExample[0]["status"]
    except KeyError:
        return None
    except IndexError:
        return None

def getOperationAmount(hash):
    print("request")
    sys.stdout.flush()
    conn = http.client.HTTPSConnection("api.ghostnet.tzkt.io")
    headers = {
        }
  
    link="/v1/operations/"+hash 
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonRes=json.loads(output)
    if (jsonRes[0]["type"]=="reveal"):
        return jsonRes[1]["amount"]
    return jsonRes[0]["amount"]
print(getOperationAmount("oop4V6HPBr85iWwXss8JiaTj9DKb3a3JXBVfuFfNpW6xvyPw4jr"))
