from pytezos import pytezos
from decimal import Decimal
from pprint import pprint
import mailSender
import operationsVisualizerMain
import sys
import json
import os
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '../keys.json')
with open(file_path) as mon_fichier:
    data = json.load(mon_fichier)
    privateKey=data["privateKeyCashBackSender"]
    publicKey=data["publicKeyCashBackSender"]

def cashbackSender(amountToSend,userAddress):
    print("trying to sendCashBack "+str(Decimal(amountToSend))+ " to "+str(userAddress))
    sys.stdout.flush()
    hash=pytezos.using(key=privateKey, shell="https://mainnet.smartpy.io") \
    .transaction(destination=userAddress, amount=Decimal(amountToSend),gas_limit=1000000) \
    .autofill().sign().inject()["hash"]
    print("sent "+str(amountToSend)+" to "+userAddress)
    sys.stdout.flush()
    balance=operationsVisualizerMain.getBalanceAddress(publicKey)
    print(balance)
    sys.stdout.flush()
    if(balance<50):
        mailSender.sendAlert("Less than 50 XTZ on payements address","Only "+str(balance)+" left.")
    return hash

def sendUNO(amount,address):
    print("trying to send "+str(amount)+" UNO to "+address+" from "+publicKey)
    sys.stdout.flush()
    amountToSend=int(amount*1000000000)
    hash=(pytezos.using(key=privateKey, shell='https://mainnet.smartpy.io') \
    .contract('KT1ErKVqEhG9jxXgUG2KGLW3bNM7zXHX8SDF').transfer([{          
        "from_": publicKey,  
        "txs": [         {  
        "to_": address,  
        "token_id": 0,  
        "amount": amountToSend
          }] }]).send().hash())
    print("sent "+str(amount)+" UNO to "+address)
    sys.stdout.flush()
    balance=operationsVisualizerMain.getBalanceUNO(publicKey)
    print(balance)
    sys.stdout.flush()

    if(balance<50):
        mailSender.sendAlert("LLess than 50 UNO on payements address","Only "+str(balance)+" left.")
    return hash
