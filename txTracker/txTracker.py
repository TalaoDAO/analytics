from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import operationsVisualizer
import model
#import cashBackSender

connection = HubConnectionBuilder()\
    .with_url('https://api.ithacanet.tzkt.io/v1/events')\
    .with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()

def analyse(data):
    #pprint(data)
    for dat in data[0]["data"]:
        try:
            if dat["parameter"]["entrypoint"]=="marketplace_transfer":
                print("hash marketplace transfer "+dat["hash"])
                initiator=dat["initiator"]["address"]
                print("model.eligible "+str(model.eligible()))
                #print("length "+str(len(model.eligible())))
                elis=model.eligible()
                for u in range(0,len(elis)):
                    eli=elis[u]
                    #print(str(eli)+" -- "+str(eli[0]))
                    print("initiator "+str(initiator))
                    if initiator==str(eli[0]):
                        amount=operationsVisualizer.getOperationAmount(dat["hash"])
                        print("tezos spent : "+str(amount))
                        hashOpe=dat["hash"]
                        entrypoint=dat["parameter"]["entrypoint"]
                        initiator=dat["initiator"]["address"]
                        print(hashOpe+" : "+entrypoint+" => "+" by "+initiator)
                        discount=eli[1]
                        disc=""
                        i=0
                        while(discount[i]!="%"):
                            disc=disc+discount[i]
                            i+=1
                            if(i==len(discount)-1):
                                break
                        print("discount "+str(disc)+"%")
                        cashBack=amount*int(disc)/100000000
                        print("cashback : "+str(cashBack))
                        print(eli)
                        typeRemuneration=eli[4]
                        amountRemuneration=eli[3]
                        if typeRemuneration=="commission":
                            print("modif")
                            remu=""
                            i=0
                            while(amountRemuneration[i]!="%"):
                                remu=remu+amountRemuneration[i]
                                print(str(remu))
                                i+=1
                                if(i==len(amountRemuneration)-1):
                                    break
                            print(str(remu))
                            print(len(remu))
                            amountRemuneration=int(remu)*amount/100000000
                        print(typeRemuneration+" "+str(amountRemuneration))
                        model.addTx(hashOpe,eli[2],initiator,'KT1CfhVyVnwLnwjfZL6dY4mRNxDVbGnZCkqa',amount,dat["timestamp"],cashBack,amountRemuneration)

                        print("cashBack: "+ str(cashBack))
                        #print(str(cashBack)+" "+str(initiator))
                        print(str(cashBack),initiator)
                        print(str(amountRemuneration),eli[5])
                        model.addPayement(hashOpe,initiator,"player",cashBack)
                        model.addPayement(hashOpe,eli[5],"affiliate",amountRemuneration)
                        #cashBackSender.cashbackSender(cashBack,initiator)
                        #cashBackSender.cashbackSender(amountRemuneration,eli[5])
                        break
                print(model.isUserTracked(initiator))
                if (model.isUserTracked(initiator)):
                    hashOpe=dat["hash"]
                    amount=operationsVisualizer.getOperationAmount(dat["hash"])
                    date=dat["timestamp"]
                    model.addFee(hashOpe,initiator,date,amount)
        except KeyError:
            print("keyError")
            pass
def init():
    print("connection established, subscribing to operations")
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
    connection.stop()
