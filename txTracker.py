import model
from pytezos import pytezos
from decimal import Decimal
print(model.eligible())
def cashbackSender():
    pytezos.using(key='edsk...', shell='babylonnet') \
    .transaction(destination='tz1...', amount=Decimal('123.456')) \
    .autofill().sign().inject()
