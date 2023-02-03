from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import modelMain
import logging
import json
import sys
logging.basicConfig(level=logging.INFO)

elis=modelMain.eligible()

def transformer(num):
    logging.info("transformer")
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
    logging.info("caught a transaction, data received = %s",json.dumps(data))
    if not data[0].get("data") :
        logging.warning('It is not a transaction object')
        return
    tx=data[0]["data"][0]    
    if(str(tx["type"])=="reveal"):
        tx=data[0]["data"][1]
    hashOpe=tx["hash"]
    initiator=tx["sender"]["address"]
    logging.info("initiator : %s", initiator)   
    entryPoint=str(tx["parameter"]["entrypoint"])
    amount=tx["amount"]/1000000
    if(entryPoint=="buy"):
        eliL=modelMain.isEligible(initiator)
        eli=eliL[0]                
        if eli[0]!=None:
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
                modelMain.addTx(hashOpe,eli[2],initiator,'KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37',amount,tx["timestamp"],cashBack,amountRemuneration,"XTZ")
                logging.info("db add tx %s", str(hashOpe))
                logging.info("cashBack: %s", str(cashBack))
                logging.info("remuneration = %s %s", str(amountRemuneration),eli[5])
                #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 
                if(modelMain.isPayementAdded(hashOpe)==False):
                    modelMain.addPayement(hashOpe,initiator,"player",cashBack,"XTZ")
                    logging.info("db add payement %s %s player %s", str(hashOpe),str(initiator),str(cashBack))
                    if(len(eli[5])==36):
                        modelMain.addPayement(hashOpe,eli[5],"affiliate",amountRemuneration,"XTZ")

                            
def init():
    logging.info("connection established, subscribing to operations")
    #connection.send('SubscribeToBlocks',[])
    #connection.send('SubscribeToHead', [])
    connection.send('SubscribeToOperations', 
                    [{'address': 'KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37', 
                      'types': 'transaction'}])


def initConnection():
    global connection
    connection = HubConnectionBuilder()\
    .with_url('https://api.tzkt.io/v1/events')\
    .with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()
    connection.on_open(init)
    connection.on("operations", analyse)
    #connection.on("head", pprint)
    connection.start()
    connection.on_error(initConnection)


connection = HubConnectionBuilder()\
    .with_url('https://api.tzkt.io/v1/events')\
    .with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()

connection.on_open(init)
connection.on("operations", analyse)
#connection.on("head", pprint)
connection.start()
connection.on_error(initConnection)

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    logging.warning('shutting down...')
    connection.stop()

