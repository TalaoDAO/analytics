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
    tx=data[0]
    hashOpe=tx["hash"]
    initiator=tx["sender"]["address"]
    entryPoint=str(tx["parameter"]["entrypoint"])
    amount=tx["amount"]/1000000
    print(amount)
    print("entrypoint "+str(tx["parameter"]["entrypoint"]))
    if(entryPoint=="buy"):
        elis=[('tz1NiySfCtftUyATTNu3cN2adQxQHjq7JUeM', 25, 3, None, None, None), ('tz1LK1kJ73YwKEd8xpkCKtACc13qQayrfAeZ', 15, 1, '5%', 'commission', '')]
        for eli in elis:
            if(tx["sender"]["address"]==eli[0]):
                discount=eli[1]
                disc=transformer(discount)
                typeRemuneration=eli[4]
                amountRemuneration=eli[3]
                cashBack=int(disc)/100*amount # verifier decimales
                if typeRemuneration=="commission":
                    remu=""
                    i=0
                    while(amountRemuneration[i]!="%"):
                        remu=remu+amountRemuneration[i]
                        print(str(remu))
                        i+=1
                        if(i==len(amountRemuneration)-1):
                            break
                    amountRemuneration=int(remu)/100*amount
                print("db add tx "+str(hashOpe),str(eli[2]),str(initiator),'KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37',str(1),str(tx["timestamp"]),str(cashBack),str(amountRemuneration))
                print("cashBack: "+ str(cashBack))
                sys.stdout.flush()
                            #print(str(cashBack)+" "+str(initiator))
                print(str(cashBack),initiator)
                sys.stdout.flush()
                print(str(amountRemuneration),eli[5])
                sys.stdout.flush()
                #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 

                print("db add payement "+str(hashOpe),str(initiator),"player",str(cashBack))


conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
headers = {
        }
  
link="/v1/operations/onphZWx15bYmPR2czVzrXEQjGHs2mYG4oJmGDHBmouyS5yFTDEA" 
conn.request("GET",link , headers=headers)
res = conn.getresponse()
data = res.read()
output=data.decode("utf-8")
jsonRes=json.loads(output)
analyse(jsonRes)