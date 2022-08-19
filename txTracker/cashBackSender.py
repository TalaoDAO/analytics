#import model
from pytezos import pytezos
from decimal import Decimal
from pprint import pprint
import mailSender
import operationsVisualizer
import sys
import json
import os
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '../keys.json')
with open(file_path) as mon_fichier:
    data = json.load(mon_fichier)
    privateKey=data["privateKeyCashBackSender"]
    print(privateKey)
    sys.stdout.flush()
    publicKey=data["publicKeyCashBackSender"]
    print(publicKey)
    sys.stdout.flush()
def cashbackSender(amountToSend,userAddress):
    print("trying to sendCashBack "+str(Decimal(amountToSend))+ " to "+str(userAddress))
    sys.stdout.flush()
    hash=pytezos.using(key=privateKey, shell="https://rpc.ghostnet.teztnets.xyz/") \
    .transaction(destination=userAddress, amount=Decimal(amountToSend),gas_limit=1000000) \
    .autofill().sign().inject()["hash"]
    print("sent "+str(amountToSend)+" to "+userAddress)
    sys.stdout.flush()
    balance=operationsVisualizer.getBalanceAddress(publicKey)
    print(balance)
    sys.stdout.flush()
    if(balance<50):
        mailSender.sendAlert("Less than 50 XTZ on payements address","Only "+str(balance)+" left.")
    return hash

    