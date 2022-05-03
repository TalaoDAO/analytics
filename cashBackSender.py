import model
from pytezos import pytezos
from decimal import Decimal
#print(model.eligible())
def cashbackSender(amountToSend,userAddress):
    print("trying to sendCashBack")
    pytezos.using(key='edskRz4RJ5H9NYiAQiP5ESmzpmT4aexBYqaxiqgW6Zxwq4zWp4H3XRj5CQdYMpjcaiFbmoq4dxJRJ27aT8LEPKArumJ8Hm3KDA', shell="https://rpczero.tzbeta.net/") \
    .transaction(destination=userAddress, amount=Decimal(amountToSend)) \
    .autofill().sign().inject()
    print("sent "+str(amountToSend)+" to "+userAddress)
#cashbackSender(0.00001,"tz1P3zm6rgzfYM3xHLv4xm9bQbQ5A74oid39")