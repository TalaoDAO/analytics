from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import operationsVisualizerMain
#print(operationsVisualizerMain.getOperationAmount("op8a6QBcK4bbfy2ZnAR7utzMgJkypQtx2arVXo5qsoKpFwgdtsv"))
import modelMain

import sys
#import cashBackSender
#print("txTrackerService")
#sys.stdout.flush()

#This service use a websocket system based on https://api.tzkt.io/#section/Python-simple-client

connection = HubConnectionBuilder()\
    .with_url('https://api.tzkt.io/v1/events')\
    .with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()


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
    pprint(data)
    for dat in data[0]["data"]:
        try:
            if dat["parameter"]["entrypoint"]=="mint":
                print("hash mint "+dat["hash"])
                sys.stdout.flush()
                #print("data from api "+str(dat))
                #sys.stdout.flush()
                initiator=dat["initiator"]["address"]
                print("modelMain.eligible "+str(modelMain.eligible()))
                sys.stdout.flush()

                print("initiator :"+initiator)
                sys.stdout.flush()
                #print("length "+str(len(modelMain.eligible())))
                elis=modelMain.eligible() # here i get vouchers with addresses of players having a voucher
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
                            modelMain.addTx(hashOpe,eli[2],initiator,'KT1CfhVyVnwLnwjfZL6dY4mRNxDVbGnZCkqa',1,dat["timestamp"],cashBack,amountRemuneration)
                            print("db add tx "+str(hashOpe),str(eli[2]),str(initiator),'KT1CfhVyVnwLnwjfZL6dY4mRNxDVbGnZCkqa',str(1),str(dat["timestamp"]),str(cashBack),str(amountRemuneration))
                            print("cashBack: "+ str(cashBack))
                            sys.stdout.flush()
                            #print(str(cashBack)+" "+str(initiator))
                            print(str(cashBack),initiator)
                            sys.stdout.flush()
                            print(str(amountRemuneration),eli[5])
                            sys.stdout.flush()
                            #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 
                            if(modelMain.isPayementAdded(hashOpe)==False):
                                modelMain.addPayement(hashOpe,initiator,"player",cashBack)
                                print("db add payement "+str(hashOpe),str(initiator),"player",str(cashBack))
                                if(len(eli[5])==36):
                                    modelMain.addPayement(hashOpe,eli[5],"affiliate",amountRemuneration)

                            break
                print("user Tracked "+str(modelMain.isUserTracked(initiator)))
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


def init():
    print("connection established, subscribing to operations")
    sys.stdout.flush()
    #connection.send('SubscribeToBlocks',[])
    #connection.send('SubscribeToHead', [])
    connection.send('SubscribeToOperations', 
                    [{'address': 'KT1JwfnnWU67BftQbHbxpqTJjkMZa9GW1JAU', 
                      'types': 'transaction'}])

connection.on_open(init)
#connection.on("head", pprint)
connection.on("operations", analyse)
#connection.on("blocks", pprint)

connection.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    print('shutting down...')
    sys.stdout.flush()
    connection.stop()