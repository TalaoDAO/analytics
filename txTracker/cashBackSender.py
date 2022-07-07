import model
from pytezos import pytezos
from decimal import Decimal
from pprint import pprint
import sys
def cashbackSender(amountToSend,userAddress):
    print("trying to sendCashBack")
    sys.stdout.flush()
    hash=pytezos.using(key='edskS7hDFoZo1pXVtCmdFxhs2z44ZrWWnNaZx1vAZqqfsowyMbXJWEqfw5rdiKQ6Uqaeiqdppvwo3nJFFUkG1sCFyTasVVfbQJ', shell="https://ghostnet.smartpy.io/") \
    .transaction(destination=userAddress, amount=Decimal(amountToSend),gas_limit=100000) \
    .autofill().sign().inject()["hash"]
    print("sent "+str(amountToSend)+" to "+userAddress)
    sys.stdout.flush()
    return hash
