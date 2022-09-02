from importlib.metadata import EntryPoint
from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import operationsVisualizerMain
import modelMain
import sys 

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

connection = HubConnectionBuilder()\
    .with_url('https://api.tzkt.io/v1/events')\
    .with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()
def analyse(data):
    tx=data[0]["data"][0]
    hashOpe=tx["hash"]
    initiator=tx["initiator"]
    entryPoint=str(tx["parameter"]["entrypoint"])
    print("entrypoint "+str(tx["parameter"]["entrypoint"]))
    if(entryPoint=="buy"):
        elis=modelMain.eligible()
        for eli in elis:
            if(tx["initiator"]==eli[0]):
                discount=eli[1]
                disc=transformer(discount)
                typeRemuneration=eli[4]
                amountRemuneration=eli[3]
                cashBack=int(disc)/100 # verifier decimales
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
                modelMain.addTx(hashOpe,eli[2],initiator,'KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37',1,tx["timestamp"],cashBack,amountRemuneration,"XTZ")
                print("db add tx "+str(hashOpe),str(eli[2]),str(initiator),'KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37',str(1),str(tx["timestamp"]),str(cashBack),str(amountRemuneration))
                print("cashBack: "+ str(cashBack))
                sys.stdout.flush()
                            #print(str(cashBack)+" "+str(initiator))
                print(str(cashBack),initiator)
                sys.stdout.flush()
                print(str(amountRemuneration),eli[5])
                sys.stdout.flush()
                #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 
                if(modelMain.isPayementAdded(hashOpe)==False):
                    modelMain.addPayement(hashOpe,initiator,"player",cashBack,"XTZ")
                    print("db add payement "+str(hashOpe),str(initiator),"player",str(cashBack))
                    if(len(eli[5])==36):
                        modelMain.addPayement(hashOpe,eli[5],"affiliate",amountRemuneration,"XTZ")

                            
def init():
    print("connection established, subscribing to blocks and operations")
    connection.send('SubscribeToOperations', 
                    [{'address': 'KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37', 
                      'types': 'transaction'}])

connection.on_open(init)
connection.on("operations", analyse)

"""connection.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    print('shutting down...')
    connection.stop()"""

print(modelMain.eligible())

