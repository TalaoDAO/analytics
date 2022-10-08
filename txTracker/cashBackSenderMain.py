from pytezos import pytezos
from decimal import Decimal
import mailSender
import operationsVisualizerMain
import json
import os
import message
import logging
logging.basicConfig(level=logging.INFO)


#NODE = "https://mainnet.smartpy.io"
NODE= "https://rpc.tzbeta.net/"

script_dir = os.path.dirname(__file__)
script_dir = os.path.dirname(script_dir)
file_path = os.path.join(script_dir, 'keys.json')

with open(file_path) as mon_fichier:
    data = json.load(mon_fichier)
    privateKey=data["privateKeyCashBackSender"]
    publicKey=data["publicKeyCashBackSender"]
    smtp_password = data["smtp_password"]
  

def cashbackSender(amount,userAddress):
    amountToSend=int(amount*1000000)
    logging.info("trying to sendCashBack %s to %s", str(amountToSend), str(userAddress))
    hash=pytezos.using(key=privateKey, shell = NODE) \
    .transaction(destination=userAddress, amount=int(amountToSend)) \
    .autofill().sign().inject()["hash"]
    logging.info("sent %s to %s", str(amountToSend), userAddress)
    balance=operationsVisualizerMain.getBalanceAddress(publicKey)
    logging.info("balance = %s", balance)
    if balance<50 :
        message_text = "Less than 50 XTZ on payements address, only " +str(balance)+" left."
        message.message("Funds needed", "thierry@altme.io", message_text, smtp_password)
    return hash


def sendUNO(amount,address):
    logging.info("trying to send %s UNO to %s from %s", str(amount), address, publicKey)
    amountToSend=int(amount*1000000000)
    logging.info("amount to send = %s", amountToSend)
    tx_data = [{"from_": publicKey,"txs": [{"to_": address,"token_id": 0,"amount": amountToSend}]}]
    hash=(pytezos.using(key=privateKey, shell=NODE) \
    .contract('KT1ErKVqEhG9jxXgUG2KGLW3bNM7zXHX8SDF').transfer(tx_data).send(gas_reserve=100).hash())
    logging.info("sent  %s UNO to %s", str(amount),address)
    balance=operationsVisualizerMain.getBalanceUNO(publicKey)
    logging.info("balance = %s", balance)
    if balance < 50 :
        message_text = "Less than 50 UNO on payements address, only " +str(balance)+" left."
        message.message("Funds needed", "thierry@altme.io", message_text, smtp_password)
    return hash
