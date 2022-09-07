import pprint
import sys
import operationsVisualizerMain
import http.client
import json
def transformer(num):
    print("transformer")
    sys.stdout.flush()
    print(num)
    sys.stdout.flush()
    sys.stdout.flush()
    if(type(num)==int):
        return num
    if(num[len(num)-1]=="%"):
        disc=""
        i=0
        while(num[i]!="%"):
            disc=disc+num[i]
            i+=1
            if(i==len(num)-1):
                break
        return int(disc)
    return int(num)
def analyse(data):
    for dat in data:
        try:
            if dat["parameter"]["entrypoint"]=="mint":
                print("hash mint "+dat["hash"])
                sys.stdout.flush()
                #print("data from api "+str(dat))
                #sys.stdout.flush()
                initiator=dat["initiator"]["address"]
                sys.stdout.flush()

                print("initiator :"+initiator)
                sys.stdout.flush()
                #print("length "+str(len(modelMain.eligible())))
                elis=[('tz1NiySfCtftUyATTNu3cN2adQxQHjq7JUeM', 25, 3, None, None, None), ('tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im', 15, 1, '5%', 'commission', '')] # here i get vouchers with addresses of players having a voucher
                #print("eligibles "+str(elis))
                #sys.stdout.flush()
                for u in range(0,len(elis)):
                    eli=elis[u]
                    #print(str(eli[0])+", initiator : "+str(initiator))
                    #sys.stdout.flush()
                    if initiator==str(eli[0]):
                        hashOpe=dat["hash"]
                        if operationsVisualizerMain.isTezotopMinted(hashOpe):
                            entrypoint=dat["parameter"]["entrypoint"]
                            initiator=dat["initiator"]["address"]
                            print(hashOpe+" : "+entrypoint+" => "+" by "+initiator)
                            sys.stdout.flush()
                            discount=eli[1]
                            disc=transformer(discount)
                            cashBack=int(disc)/100 # verifier decimales
                            typeRemuneration=eli[4]
                            amountRemuneration=eli[3]
                            if typeRemuneration=="commission":
                                remu=""
                                i=0
                                while(amountRemuneration[i]!="%"):
                                    remu=remu+amountRemuneration[i]
                                    print(str(remu))
                                    i+=1
                                    if(i==len(amountRemuneration)-1):
                                        break
                                amountRemuneration=int(remu)/100
                            #here i add a transaction in the db 
                            print("db add tx "+str(hashOpe),str(eli[2]),str(initiator),'KT1H67aLf6SUN1BysWfFLfjUEuN1M6E9qFwM',str(1),str(dat["timestamp"]),str(cashBack),str(amountRemuneration))
                            print("cashBack: "+ str(cashBack))
                            sys.stdout.flush()
                            #print(str(cashBack)+" "+str(initiator))
                            print(str(cashBack),initiator)
                            sys.stdout.flush()
                            print(str(amountRemuneration),eli[5])
                            sys.stdout.flush()
                            #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 

                            break
                        
                sys.stdout.flush()
                #here i track all transactions made by an user talao brang to Tezotopia ACTUALLY NOT EFFECTIVE
                """if (modelMain.isUserTracked(initiator)):
                    hashOpe=dat["hash"]
                    #amount=operationsVisualizerMain.getOperationAmount(dat["hash"])
                    date=dat["timestamp"]
                    if(modelMain.isFeeAdded(hashOpe)==False):
                        modelMain.addFee(hashOpe,initiator,date,1)"""
        except KeyError:
            print("keyError")
            sys.stdout.flush()
            pass

conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
headers = {
        }
  
link="/v1/operations/opEd1dYuSAHEZ9etSuJ9XeJFu6UfnrQVvCy6h2p7mMsSuTJKhcK" 
conn.request("GET",link , headers=headers)
res = conn.getresponse()
data = res.read()
output=data.decode("utf-8")
jsonRes=json.loads(output)
analyse(jsonRes)