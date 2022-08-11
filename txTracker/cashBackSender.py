import model
from pytezos import pytezos
from decimal import Decimal
from pprint import pprint
import mailSender
import operationsVisualizer
import sys
def cashbackSender(amountToSend,userAddress):
    print("trying to sendCashBack")
    sys.stdout.flush()
    hash=pytezos.using(key=privateKey, shell="https://ghostnet.smartpy.io/") \
    .transaction(destination=userAddress, amount=Decimal(amountToSend),gas_limit=100000) \
    .autofill().sign().inject()["hash"]
    print("sent "+str(amountToSend)+" to "+userAddress)
    sys.stdout.flush()
    balance=operationsVisualizer.getBalanceAddress(publicKey)
    if(balance<50):
        mailSender.sendAlert("Less than 50 XTZ on payements address","Only "+str(balance)+" left.")
    return hash
