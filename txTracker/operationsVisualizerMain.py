import http.client
from datetime import datetime
import json
from pprint import pprint
import sys


def getOperationStatus(hash):

    conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
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
    conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
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

def getBalanceAddress(address):
    print("request balance "+address)
    sys.stdout.flush()
    conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
    headers = {
        }
  
    link="/v1/accounts/"+address+"/balance"
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonRes=json.loads(output)
    print(int(jsonRes)/1000000)
    return(int(jsonRes)/1000000)
def getBalanceUNO(address):
    print("request balance ")
    sys.stdout.flush()
    conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
    headers = {
        }
  
    link="/v1/tokens/balances?token.contract=KT1ErKVqEhG9jxXgUG2KGLW3bNM7zXHX8SDF&account="+address+"&token.tokenId=0"
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonRes=json.loads(output)
    return(int(jsonRes[0]["balance"])/1000000000)
def isTezotopMinted(hash):
    conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
    headers = {
        }
  
    link="/v1/operations/"+hash
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonRes=json.loads(output)
    try:
        print(jsonRes[8]["diffs"][1]["content"]["value"]["category"])
        return jsonRes[8]["diffs"][1]["content"]["value"]["category"]=="tezotop"
    except IndexError:
        return False
def isArtifactFromStarbaseMinted(hash):
    conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
    headers = {
        }
  
    link="/v1/operations/"+hash
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonRes=json.loads(output)
    #pprint(jsonRes)
    try:
        print(jsonRes[3]["diffs"][1]["content"]["value"]["category"])
        return jsonRes[3]["diffs"][1]["content"]["value"]["category"]=="artifact"
    except IndexError:
        return False
def getAmountPrimarySales(hash):
    conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
    headers = {
        }
  
    link="/v1/operations/"+hash
    conn.request("GET",link , headers=headers)
    res = conn.getresponse()
    data = res.read()
    output=data.decode("utf-8")
    jsonRes=json.loads(output)
    try:
        print(int(jsonRes[0]["diffs"][1]["content"]["value"]["price"]))
        return int(jsonRes[0]["diffs"][1]["content"]["value"]["price"])
    except IndexError:
        return None
    except KeyError:
        return None
#print(getBalanceUNO("tz1UJEY6MH5KaDtYdLycoCGB7z1zDq8Krfhy"))
#print(isTezotopMinted("ooD1tmwxtty6Gi4p3veJF5QDKSqcUKTLFrr5iYTCJauFpYQo87a"))
#print(isArtifactFromStarbaseMinted("oo7RBQSgBx35PzKACxsiG1bujswM3ooEs4pY5BA3m3pxePgZbZf"))
print(getAmountPrimarySales("ooGpTGhDxWo7o4fjT2vMfLxsrGhVet7Z7UHZ1BZT9VAinZJUbfK"))