import http.client
from datetime import datetime
import json


def tsAPItoTsPy(date):  #allows to convert timestamp format of the api to a python datetime object to compare them numerically
    year=int(date[0]+date[1]+date[2]+date[3])
    month=int(date[5]+date[6])
    day=int(date[8]+date[9])
    hour=int(date[11]+date[12])
    minutes=int(date[14]+date[15])
    seconds=int(date[17]+date[18])
    return(datetime.timestamp(datetime(year, month, day, hour, minutes,seconds)))
def main():
    addresses=["tz1gNDd435vP9qppaZMD5yuCkiQua9zSvcod","tz1aMMC3iPNbfB7C8dNJ3Mf74L7xERXJ9A8q"]
    smartsContracts=["KT1Prt13ado1iDMWKDEY5eunrjGuwbCoABWr","KT1LLKbQe5rJ4yY7PuH2T9xTCbnWaFc7wHRs"]
    timestampStart="2022-04-06T01:18:59Z"
    #timestampEnd="2022-04-10T00:00:00Z"
    timestampEnd="2022-04-14T00:00:00Z"
    conn = http.client.HTTPSConnection("api.tzkt.io")
    headers = {
        }
    result=[]
    for sc in smartsContracts:  
        for ad in addresses:
            link="/v1/accounts/"+sc+"/operations?entrypoint=mint&sender.eq="+ad+"&timestamp.ge="+timestampStart 
            conn.request("GET",link , headers=headers)
            res = conn.getresponse()
            data = res.read()
            output=data.decode("utf-8")
            jsonExample=json.loads(output)
            for u in range (0,len(jsonExample)):
                if tsAPItoTsPy(jsonExample[u]['timestamp'])<tsAPItoTsPy(timestampEnd): #verifying that the tx happened before the timestampEnd
                    result.append(jsonExample[u])

    #print(result)
    print(str(len(result))+" tx found")
    with open('json_data.json', 'w') as mon_fichier:
        json.dump(result, mon_fichier)
    return result