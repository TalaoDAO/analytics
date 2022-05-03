from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import operationsVisualizer
import model
import cashBackSender

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
                print("length "+str(len(model.eligible())))
                elis=model.eligible()
                for u in range(0,len(elis)):
                    eli=elis[u]
                    print(str(eli)+" -- "+str(eli[0]))
                    print("initiator "+str(initiator))
                    if initiator==str(eli[0]):
                        amount=operationsVisualizer.getOperationAmount(dat["hash"])
                        print(amount)
                        hashOpe=dat["hash"]
                        entrypoint=dat["parameter"]["entrypoint"]
                        initiator=dat["initiator"]["address"]
                        print(hashOpe+" : "+entrypoint+" => "+" by "+initiator)
                        print(amount)
                        print(eli[1])
                        discount=eli[1]
                        print(discount)
                        print("discount "+str(discount)+"%")

                        model.addTx(hashOpe,eli[2],initiator,'KT1CfhVyVnwLnwjfZL6dY4mRNxDVbGnZCkqa',amount,dat["timestamp"])

                        cashBack=amount*eli[1]/100000000
                        print("cashBack: "+ str(amount*eli[1]/100000000))
                        print(str(cashBack)+" "+str(initiator))
                        print(cashBack,initiator)
                        
                        cashBackSender.cashbackSender(cashBack,initiator)
                print("fin loop")
        except KeyError:
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
