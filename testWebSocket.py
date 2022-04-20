from signalrcore.hub_connection_builder import HubConnectionBuilder
from time import sleep
from pprint import pprint
import operationsVisualizer
import model
connection = HubConnectionBuilder()\
    .with_url('https://api.hangzhounet.tzkt.io/v1/events')\
    .with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()
def analyse(data):
    #pprint(data)
    for dat in data[0]["data"]:
        #print(dat["parameter"]["entrypoint"])
        if dat["parameter"]["entrypoint"]=="marketplace_transfer":
            print(dat["hash"])
            initiator=dat["initiator"]["address"]
            for eli in model.eligible().items():
                print(eli)
                print(eli[0])
                print(eli[0]==initiator)
                print(initiator)
                if initiator==eli[0]:
                    amount=operationsVisualizer.getOperationAmount(dat["hash"])
                    hashOpe=dat["hash"]
                    entrypoint=dat["parameter"]["entrypoint"]
                    initiator=dat["initiator"]["address"]
                    print(hashOpe+" : "+entrypoint+" => "+" by "+initiator)
                    print(amount)
                    model.addTx(hashOpe,eli[1],initiator,'KT1JWMAHDuUMr82nQvS9AxEXyKU8MAeez4Ro',amount,dat["timestamp"])
def init():
    print("connection established, subscribing to operations")
    #connection.send('SubscribeToBlocks',[])
    #connection.send('SubscribeToHead', [])
    connection.send('SubscribeToOperations', 
                    [{'address': 'KT1JWMAHDuUMr82nQvS9AxEXyKU8MAeez4Ro', 
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
