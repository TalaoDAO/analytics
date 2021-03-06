from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import operationsVisualizer
#print(operationsVisualizer.getOperationAmount("op8a6QBcK4bbfy2ZnAR7utzMgJkypQtx2arVXo5qsoKpFwgdtsv"))
import model
print(model.eligible())
import sys
#import cashBackSender
#print("txTrackerService")
#sys.stdout.flush()

#This service use a websocket system based on https://api.tzkt.io/#section/Python-simple-client

connection = HubConnectionBuilder()\
    .with_url('https://api.ithacanet.tzkt.io/v1/events')\
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
    #pprint(data)
    for dat in data[0]["data"]:
        try:
            if dat["parameter"]["entrypoint"]=="marketplace_transfer":
                print("hash marketplace transfer "+dat["hash"])
                sys.stdout.flush()
                print("data from api "+str(dat))
                sys.stdout.flush()
                initiator=dat["initiator"]["address"]
                #print("model.eligible "+str(model.eligible()))
                print("initiator :"+initiator)
                sys.stdout.flush()
                #print("length "+str(len(model.eligible())))
                elis=model.eligible() # here i get vouchers with addresses of players having a voucher
                print("eligibles "+str(elis))
                sys.stdout.flush()
                for u in range(0,len(elis)):
                    eli=elis[u]
                    #print(str(eli)+" -- "+str(eli[0]))
                    print("initiator "+str(initiator))
                    sys.stdout.flush()
                    if initiator==str(eli[0]):
                        print("yes")
                        sys.stdout.flush()
                        amount=operationsVisualizer.getOperationAmount(dat["hash"])
                        print("tezos spent : "+str(amount))
                        sys.stdout.flush()
                        hashOpe=dat["hash"]
                        entrypoint=dat["parameter"]["entrypoint"]
                        initiator=dat["initiator"]["address"]
                        print(hashOpe+" : "+entrypoint+" => "+" by "+initiator)
                        sys.stdout.flush()
                        discount=eli[1]
                        print(discount)
                        sys.stdout.flush()
                        disc=transformer(discount)
                        print("discount "+str(disc)+"%")
                        sys.stdout.flush()
                        cashBack=amount*int(disc)/100000000
                        print("cashback : "+str(cashBack))
                        sys.stdout.flush()
                        print(eli)
                        sys.stdout.flush()
                        typeRemuneration=eli[4]
                        amountRemuneration=eli[3]
                        if typeRemuneration=="commission":
                            print("modif")
                            sys.stdout.flush()
                            remu=""
                            i=0
                            while(amountRemuneration[i]!="%"):
                                remu=remu+amountRemuneration[i]
                                print(str(remu))
                                i+=1
                                if(i==len(amountRemuneration)-1):
                                    break
                            print(str(remu))
                            sys.stdout.flush()
                            print(len(remu))
                            sys.stdout.flush()
                            amountRemuneration=int(remu)*amount/100000000
                        print(typeRemuneration+" "+str(amountRemuneration))
                        sys.stdout.flush()
                        #here i add a transaction in the db 
                        model.addTx(hashOpe,eli[2],initiator,'KT1CfhVyVnwLnwjfZL6dY4mRNxDVbGnZCkqa',amount,dat["timestamp"],cashBack,amountRemuneration)

                        print("cashBack: "+ str(cashBack))
                        sys.stdout.flush()
                        #print(str(cashBack)+" "+str(initiator))
                        print(str(cashBack),initiator)
                        sys.stdout.flush()
                        print(str(amountRemuneration),eli[5])
                        sys.stdout.flush()
                        #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 
                        if(model.isPayementAdded(hashOpe)==False):
                            model.addPayement(hashOpe,initiator,"player",cashBack)
                            if(len(eli[5])==36):
                                model.addPayement(hashOpe,eli[5],"affiliate",amountRemuneration)
                        #cashBackSender.cashbackSender(cashBack,initiator)
                        #cashBackSender.cashbackSender(amountRemuneration,eli[5])
                        break
                print("user Tracked "+str(model.isUserTracked(initiator)))
                sys.stdout.flush()
                #here i track all transactions made by an user talao brang to Tezotopia
                if (model.isUserTracked(initiator)):
                    hashOpe=dat["hash"]
                    amount=operationsVisualizer.getOperationAmount(dat["hash"])
                    date=dat["timestamp"]
                    if(model.isFeeAdded(hashOpe)==False):
                        model.addFee(hashOpe,initiator,date,amount)
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
                    [{'address': 'KT1CfhVyVnwLnwjfZL6dY4mRNxDVbGnZCkqa', 
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
