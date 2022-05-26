from jsonschema import ValidationError
from pytezos import pytezos
pytezos.using(shell="https://mainnet.api.tez.ie")
pytezos.shell.node.uri[0]="https://mainnet.api.tez.ie"
#print(pytezos.shell.node.uri[0])
#print(pytezos)

contractView=pytezos.contract(address="KT1ViVwoVfGSCsDaxjwoovejm1aYSGz7s2TZ") # nft registery address

print(contractView._get_token_metadata(55555)) # here 55555 is the id of the nft we want to see


#print(contractView)
