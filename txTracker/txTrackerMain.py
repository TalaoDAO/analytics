from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import operationsVisualizerMain
#print(operationsVisualizerMain.getOperationAmount("op8a6QBcK4bbfy2ZnAR7utzMgJkypQtx2arVXo5qsoKpFwgdtsv"))
import modelMain
import logging
logging.basicConfig(level=logging.INFO)
import sys
import json


#This service use a websocket system based on https://api.tzkt.io/#section/Python-simple-client
# follow Tezotopia Minter  


def transformer(num):
    logging.info("call transformer")
    sys.stdout.flush()
    logging.info("num = %s", num)
    if(type(num)==int):
        return num
    if(num[len(num)-1]=="%") :
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
    logging.info("caught a tx")
    logging.info("data = %s", json.dumps(data))
    if not data[0].get("data") :
        logging.warning('not a transaction object')
        return
    for dat in data[0].get["data"]:
        try:
            if dat["parameter"]["entrypoint"]=="mint":
                logging.info("hash mint %s", dat["hash"])
                initiator=dat["initiator"]["address"]
                logging.info("initiator : %s", initiator)
                eliL=modelMain.isEligible(initiator)
                eli=eliL[0]                
                if eli[0] :
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
                            modelMain.addTx(hashOpe,eli[2],initiator,'KT1H67aLf6SUN1BysWfFLfjUEuN1M6E9qFwM',1,dat["timestamp"],cashBack,amountRemuneration,"UNO")
                            print("db add tx ", str(hashOpe) , str(eli[2]) , str(initiator) ,'KT1H67aLf6SUN1BysWfFLfjUEuN1M6E9qFwM' , str(1) , str(dat["timestamp"]) , str(cashBack) , str(amountRemuneration))
                            logging.info("cashBack = %s", str(cashBack))
                            #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 
                            if(modelMain.isPayementAdded(hashOpe)==False):
                                modelMain.addPayement(hashOpe,initiator,"player",cashBack,"UNO")
                                print("db add payement "+str(hashOpe),str(initiator),"player",str(cashBack))
                                if(len(eli[5])==36):
                                    modelMain.addPayement(hashOpe,eli[5],"affiliate",amountRemuneration,"UNO")
                            break

                    if operationsVisualizerMain.isArtifactFromStarbaseMinted(hashOpe):
                            entrypoint=dat["parameter"]["entrypoint"]
                            initiator=dat["initiator"]["address"]
                            print(hashOpe+" : "+entrypoint+" => "+" by "+initiator)
                            discount=eli[1]
                            disc=transformer(discount)
                            cashBack=int(disc)/1000 # verifier decimales
                            typeRemuneration=eli[4]
                            amountRemuneration=eli[3]
                            if typeRemuneration=="commission":
                                remu=""
                                i=0
                                while(amountRemuneration[i]!="%"):
                                    remu=remu+amountRemuneration[i]
                                    i+=1
                                    if(i==len(amountRemuneration)-1):
                                        break
                                amountRemuneration=int(remu)/1000
                            #here i add a transaction record in the db 
                            modelMain.addTx(hashOpe,eli[2],initiator,'KT1H67aLf6SUN1BysWfFLfjUEuN1M6E9qFwM',0.1,dat["timestamp"],cashBack,amountRemuneration,"UNO")
                            print("db add tx "+str(hashOpe),str(eli[2]),str(initiator),'KT1H67aLf6SUN1BysWfFLfjUEuN1M6E9qFwM',str(1),str(dat["timestamp"]),str(cashBack),str(amountRemuneration))
                            logging.info("cashBack = %s", str(cashBack))
                            print(str(cashBack),initiator)
                            #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 
                            if(modelMain.isPayementAdded(hashOpe)==False):
                                modelMain.addPayement(hashOpe,initiator,"player",cashBack,"UNO")
                                print("db add payement "+str(hashOpe),str(initiator),"player",str(cashBack))
                                if(len(eli[5])==36):
                                    modelMain.addPayement(hashOpe,eli[5],"affiliate",amountRemuneration,"UNO")
                            break
                        
                logging.info("user Tracked = %s", str(modelMain.isUserTracked(initiator)))
                #here i track all transactions made by an user talao brang to Tezotopia ACTUALLY NOT EFFECTIVE
                """if (modelMain.isUserTracked(initiator)):
                    hashOpe=dat["hash"]
                    #amount=operationsVisualizerMain.getOperationAmount(dat["hash"])
                    date=dat["timestamp"]
                    if(modelMain.isFeeAdded(hashOpe)==False):
                        modelMain.addFee(hashOpe,initiator,date,1)"""
        except KeyError:
            logging.error("keyError")
    return


def init():
    #connection.send('SubscribeToHead', [])
    connection.send('SubscribeToOperations', 
                    [{'address': 'KT1H67aLf6SUN1BysWfFLfjUEuN1M6E9qFwM', 
                      'types': 'transaction'}])

# main script
try :
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
    logging.info("Connection TZKT initialized")
except :
    logging.error("connexion failed to initialize")
    connection.stop()
    sys.exit()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
        logging.error("Interruption keyboard")
finally:
    logging.warning('shutting down...')
    connection.stop()