import model
from pytezos import pytezos
from decimal import Decimal
from pprint import pprint
#print(model.eligible())
def cashbackSender(amountToSend,userAddress):
    print("trying to sendCashBack")
    hash=pytezos.using(key='edskS7hDFoZo1pXVtCmdFxhs2z44ZrWWnNaZx1vAZqqfsowyMbXJWEqfw5rdiKQ6Uqaeiqdppvwo3nJFFUkG1sCFyTasVVfbQJ', shell="https://ithacanet.smartpy.io/") \
    .transaction(destination=userAddress, amount=Decimal(amountToSend)) \
    .autofill().sign().inject()["hash"]
    print("sent "+str(amountToSend)+" to "+userAddress)
    return hash
#print(cashbackSender(0.00001,"tz1P3zm6rgzfYM3xHLv4xm9bQbQ5A74oid39"))