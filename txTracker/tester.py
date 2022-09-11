import pprint
import sys
#import operationsVisualizerMain
import http.client
import json
import model
def transformer(num):
    print("transformer")
    sys.stdout.flush()
    print(num)
    sys.stdout.flush()
    sys.stdout.flush()
    if(type(num)==int):
        return num
    if(num[len(num)-1]=="%"):
        disc=""
        i=0
        while(num[i]!="%"):
            disc=disc+num[i]
            i+=1
            if(i==len(num)-1):
                break
        return int(disc)
    return int(num)

def analyse(data):
    tx=data[0]["data"][0]
    hashOpe=tx["hash"]
    initiator=tx["sender"]["address"]
    entryPoint=str(tx["parameter"]["entrypoint"])
    amount=tx["amount"]/1000000
    print(amount)
    print("entrypoint "+str(tx["parameter"]["entrypoint"]))
    if(entryPoint=="buy"):
        elis=[('tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK', 25, 3, None, None, None), ('tz1LK1kJ73YwKEd8xpkCKtACc13qQayrfAeZ', 15, 1, '5%', 'commission', '')]
        for eli in elis:
            if(tx["sender"]["address"]==eli[0]):
                discount=eli[1]
                disc=transformer(discount)
                typeRemuneration=eli[4]
                amountRemuneration=eli[3]
                cashBack=int(disc)/100*amount # verifier decimales
                if typeRemuneration=="commission":
                    remu=""
                    i=0
                    while(amountRemuneration[i]!="%"):
                        remu=remu+amountRemuneration[i]
                        print(str(remu))
                        i+=1
                        if(i==len(amountRemuneration)-1):
                            break
                    amountRemuneration=int(remu)/100*amount
                print("db add tx "+str(hashOpe),str(eli[2]),str(initiator),'KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37',str(1),str(tx["timestamp"]),str(cashBack),str(amountRemuneration))
                print("cashBack: "+ str(cashBack))
                sys.stdout.flush()
                            #print(str(cashBack)+" "+str(initiator))
                print(str(cashBack),initiator)
                sys.stdout.flush()
                print(str(amountRemuneration),eli[5])
                sys.stdout.flush()
                #here i add to the pile/stack in the db a new waiting paiement for the player and one for the affiliate 

                print("db add payement "+str(hashOpe),str(initiator),"player",str(cashBack))


"""conn = http.client.HTTPSConnection("api.mainnet.tzkt.io")
headers = {
        }
  
link="/v1/operations/opLXjJnDkenT3j42atB7hPvo49yoXoaoQ8XDCWAJHoeh6ybAy1W" 
conn.request("GET",link , headers=headers)
res = conn.getresponse()
data = res.read()
output=data.decode("utf-8")
jsonRes=json.loads(output)
analyse(jsonRes)"""
"""analyse([
    {
        "type": 1,
        "data": [
            {
                "type": "transaction",
                "id": 336356948,
                "level": 2692112,
                "timestamp": "2022-09-08T09: 20: 44Z",
                "block": "BMQxzHfoswDFnpasY3GFs13bd8BN7W3eRWNNPvmGb336hB4naTy",
                "hash": "ongT6iuyNyPVJ8QRC1XzVrzGGWCX1dHraTxm6tncYXibJ1M8XAG",
                "counter": 67225521,
                "sender": {
                    "address": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK"
                },
                "gasLimit": 21210,
                "gasUsed": 12216,
                "storageLimit": 0,
                "storageUsed": 0,
                "bakerFee": 2574,
                "storageFee": 0,
                "allocationFee": 0,
                "target": {
                    "alias": "Tezotopia Primary Sales",
                    "address": "KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37"
                },
                "targetCodeHash": 589893206,
                "amount": 16000000,
                "parameter": {
                    "entrypoint": "buy",
                    "value": {
                        "receiver": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK",
                        "signature": "edsigtqnSdtX4VNN8nyJQhNjsJUcAZpGgD2oSSfv2ZSgKPnfxyQx6RcApFcoUQhiGei2wtkW7bnCkqWjaYLJs5YxTGRpfzPGu6y",
                        "listing_id": "174"
                    }
                },
                "storage": {
                    "admin": "tz1VPZyh4ZHjDDpgvznqQQXUCLcV7g91WGMz",
                    "paused": False,
                    "signer": "edpkuLxm6gqkKWEuLgXx6kuGpbbwDkjubxpzcJuNf8BP5ofHjGLshs",
                    "tokens": 188289,
                    "counter": 188286,
                    "listing": 188287,
                    "managers": [
                        "tz1bKM4FRgAsGdDWzXs4o5HZdjBbLMbPBAA1"
                    ],
                    "metadata": 188288,
                    "collector": "tz1bKM4FRgAsGdDWzXs4o5HZdjBbLMbPBAA1",
                    "royalties": {
                        "unit": {
                            "tz1UPF5vXnLLRyXLdiSJcdxKvYVzaG5S8vVV": "5000"
                        }
                    },
                    "gif_staking": {
                        "address": "KT1BJmsK1zhLy5PZNgC7YDfdjciAVTw1A5gq",
                        "discount": "300",
                        "discount_tier": "2",
                        "revenue_share": "300",
                        "tier_unlock_time": "2592000"
                    },
                    "nft_registry": "KT1ViVwoVfGSCsDaxjwoovejm1aYSGz7s2TZ",
                    "total_listing": "182",
                    "callback_expected": False,
                    "current_listing_id": None
                },
                "diffs": [
                    {
                        "bigmap": 188289,
                        "path": "tokens",
                        "action": "remove_key",
                        "content": {
                            "hash": "expruvZ1QnMqDxejwRw5ucCKPB6o7g4GJbQnFmdUAnT2WgyaPPjgcE",
                            "key": "95900",
                            "value": True
                        }
                    },
                    {
                        "bigmap": 188287,
                        "path": "listing",
                        "action": "update_key",
                        "content": {
                            "hash": "exprvTBB3SwBVLmHXtq5hEUVWbwg6FEevtAdJivXdEybPSzZDwBzrG",
                            "key": "174",
                            "value": {
                                "price": "16000000",
                                "tokens": [
                                    "95901",
                                    "95902",
                                    "95903",
                                    "95904",
                                    "95905",
                                    "95906",
                                    "95907",
                                    "95908",
                                    "95909",
                                    "95910",
                                    "95911",
                                    "95912",
                                    "95913",
                                    "95914",
                                    "95915",
                                    "95916",
                                    "95917",
                                    "95918",
                                    "95919",
                                    "95920",
                                    "95921",
                                    "95922",
                                    "95923",
                                    "95924",
                                    "95925",
                                    "95926",
                                    "95927",
                                    "95928",
                                    "95929",
                                    "95930",
                                    "95931",
                                    "95932",
                                    "95933",
                                    "95934",
                                    "95935",
                                    "95936",
                                    "95937",
                                    "95938",
                                    "95939",
                                    "95940",
                                    "95941",
                                    "95942",
                                    "95943",
                                    "95944",
                                    "95945",
                                    "95946",
                                    "95947",
                                    "95948",
                                    "95949",
                                    "95950",
                                    "95951",
                                    "95952",
                                    "95953",
                                    "95954",
                                    "95955",
                                    "95956",
                                    "95957",
                                    "95958",
                                    "95959",
                                    "95960",
                                    "95961",
                                    "95962",
                                    "95963",
                                    "95964",
                                    "95965",
                                    "95966",
                                    "95967",
                                    "95968",
                                    "95969",
                                    "95970",
                                    "95971",
                                    "95972",
                                    "95973",
                                    "95974",
                                    "95975",
                                    "95976"
                                ],
                                "category": "unit"
                            }
                        }
                    },
                    {
                        "bigmap": 188286,
                        "path": "counter",
                        "action": "update_key",
                        "content": {
                            "hash": "exprupkeTjgdTrpc4ELBrvuqHCTkhWJBHs7cQRK7dYKpenhg3Fg1bp",
                            "key": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK",
                            "value": "3"
                        }
                    }
                ],
                "status": "applied",
                "hasInternals": True
            },
            {
                "type": "transaction",
                "id": 336356949,
                "level": 2692112,
                "timestamp": "2022-09-08T09: 20: 44Z",
                "block": "BMQxzHfoswDFnpasY3GFs13bd8BN7W3eRWNNPvmGb336hB4naTy",
                "hash": "ongT6iuyNyPVJ8QRC1XzVrzGGWCX1dHraTxm6tncYXibJ1M8XAG",
                "counter": 67225521,
                "initiator": {
                    "address": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK"
                },
                "sender": {
                    "alias": "Tezotopia Primary Sales",
                    "address": "KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37"
                },
                "senderCodeHash": 589893206,
                "nonce": 8,
                "gasLimit": 0,
                "gasUsed": 1450,
                "storageLimit": 0,
                "storageUsed": 0,
                "bakerFee": 0,
                "storageFee": 0,
                "allocationFee": 0,
                "target": {
                    "address": "tz1UPF5vXnLLRyXLdiSJcdxKvYVzaG5S8vVV"
                },
                "amount": 8000000,
                "status": "applied",
                "hasInternals": False
            },
            {
                "type": "transaction",
                "id": 336356950,
                "level": 2692112,
                "timestamp": "2022-09-08T09: 20: 44Z",
                "block": "BMQxzHfoswDFnpasY3GFs13bd8BN7W3eRWNNPvmGb336hB4naTy",
                "hash": "ongT6iuyNyPVJ8QRC1XzVrzGGWCX1dHraTxm6tncYXibJ1M8XAG",
                "counter": 67225521,
                "initiator": {
                    "address": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK"
                },
                "sender": {
                    "alias": "Tezotopia Primary Sales",
                    "address": "KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37"
                },
                "senderCodeHash": 589893206,
                "nonce": 9,
                "gasLimit": 0,
                "gasUsed": 1223,
                "storageLimit": 0,
                "storageUsed": 0,
                "bakerFee": 0,
                "storageFee": 0,
                "allocationFee": 0,
                "target": {
                    "alias": "GIF staking",
                    "address": "KT1BJmsK1zhLy5PZNgC7YDfdjciAVTw1A5gq"
                },
                "targetCodeHash": -334355047,
                "amount": 480000,
                "storage": {
                    "admin": "tz1VPZyh4ZHjDDpgvznqQQXUCLcV7g91WGMz",
                    "ledger": 60449,
                    "paused": False,
                    "revenue": {
                        "total_gif": "29491564575696348",
                        "multiplier": "100000000000000000000",
                        "last_update": "2022-09-08T09: 01: 44Z",
                        "xtz_per_gif": "129139752384570",
                        "current_cycle": {
                            "revenue": "464943203",
                            "end_time": "2022-09-18T15: 00: 00Z",
                            "start_time": "2022-08-19T15: 00: 00Z",
                            "xtz_per_sec": "28329073070987654320987"
                        },
                        "cycle_duration": "2592000"
                    },
                    "staking": {
                        "gif": {
                            "address": "KT1XTxpQvo7oRCqp85LikEZgAZ22uDxhbWJv",
                            "token_id": "0"
                        },
                        "collector": "tz1bKM4FRgAsGdDWzXs4o5HZdjBbLMbPBAA1",
                        "unlock_fees": {
                            "1296000": "4000",
                            "2592000": "1000",
                            "3888000": "500"
                        },
                        "revenue_tier": "3",
                        "min_lock_amount": {
                            "1": "5000000000000",
                            "2": "25000000000000",
                            "3": "100000000000000"
                        }
                    },
                    "metadata": 60450
                },
                "status": "applied",
                "hasInternals": False
            },
            {
                "type": "transaction",
                "id": 336356951,
                "level": 2692112,
                "timestamp": "2022-09-08T09: 20: 44Z",
                "block": "BMQxzHfoswDFnpasY3GFs13bd8BN7W3eRWNNPvmGb336hB4naTy",
                "hash": "ongT6iuyNyPVJ8QRC1XzVrzGGWCX1dHraTxm6tncYXibJ1M8XAG",
                "counter": 67225521,
                "initiator": {
                    "address": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK"
                },
                "sender": {
                    "alias": "Tezotopia Primary Sales",
                    "address": "KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37"
                },
                "senderCodeHash": 589893206,
                "nonce": 10,
                "gasLimit": 0,
                "gasUsed": 1450,
                "storageLimit": 0,
                "storageUsed": 0,
                "bakerFee": 0,
                "storageFee": 0,
                "allocationFee": 0,
                "target": {
                    "address": "tz1bKM4FRgAsGdDWzXs4o5HZdjBbLMbPBAA1"
                },
                "amount": 7520000,
                "status": "applied",
                "hasInternals": False
            },
            {
                "type": "transaction",
                "id": 336356952,
                "level": 2692112,
                "timestamp": "2022-09-08T09: 20: 44Z",
                "block": "BMQxzHfoswDFnpasY3GFs13bd8BN7W3eRWNNPvmGb336hB4naTy",
                "hash": "ongT6iuyNyPVJ8QRC1XzVrzGGWCX1dHraTxm6tncYXibJ1M8XAG",
                "counter": 67225521,
                "initiator": {
                    "address": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK"
                },
                "sender": {
                    "alias": "Tezotopia Primary Sales",
                    "address": "KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37"
                },
                "senderCodeHash": 589893206,
                "nonce": 11,
                "gasLimit": 0,
                "gasUsed": 4771,
                "storageLimit": 0,
                "storageUsed": 0,
                "bakerFee": 0,
                "storageFee": 0,
                "allocationFee": 0,
                "target": {
                    "alias": "Tezotopia NFT Registry",
                    "address": "KT1ViVwoVfGSCsDaxjwoovejm1aYSGz7s2TZ"
                },
                "targetCodeHash": -60362261,
                "amount": 0,
                "parameter": {
                    "entrypoint": "transfer",
                    "value": [
                        {
                            "txs": [
                                {
                                    "to_": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK",
                                    "amount": "1",
                                    "token_id": "95900"
                                }
                            ],
                            "from_": "KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37"
                        }
                    ]
                },
                "storage": {
                    "uids": {
                        "unit": "20871",
                        "ticket": "2275",
                        "tezotop": "12236",
                        "artifact": "42585",
                        "collectible": "18100"
                    },
                    "ledger": 9920,
                    "minter": "KT1H67aLf6SUN1BysWfFLfjUEuN1M6E9qFwM",
                    "paused": False,
                    "manager": "KT1JyCbTDUgoBcErvipCsye6tu45pjUViSr2",
                    "metadata": 9921,
                    "operators": 9922,
                    "all_tokens": "96227",
                    "marketplace": "KT1PSUKkif8KZzSeWdPewWMkx61QBR8VuXsm",
                    "administrator": "tz1VPZyh4ZHjDDpgvznqQQXUCLcV7g91WGMz",
                    "pending_admin": None,
                    "token_metadata": 9924,
                    "token_attributes": 9923
                },
                "diffs": [
                    {
                        "bigmap": 9923,
                        "path": "token_attributes",
                        "action": "update_key",
                        "content": {
                            "hash": "expruvZ1QnMqDxejwRw5ucCKPB6o7g4GJbQnFmdUAnT2WgyaPPjgcE",
                            "key": "95900",
                            "value": {
                                "uid": "20690",
                                "ints": {
                                    "hp": "6",
                                    "exp": "0",
                                    "speed": "2",
                                    "attack": "3",
                                    "defence": "3",
                                    "accuracy": "3",
                                    "mint_time": "1661702999"
                                },
                                "sets": {},
                                "owner": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK",
                                "on_sale": False,
                                "strings": {
                                    "type": "land"
                                },
                                "category": "unit",
                                "token_id": "95900"
                            }
                        }
                    },
                    {
                        "bigmap": 9920,
                        "path": "ledger",
                        "action": "update_key",
                        "content": {
                            "hash": "exprudTPvxSoXqWFURazgxrSRFbVdtePAM7fXpKUqfmCm3NENr3hhz",
                            "key": {
                                "nat": "95900",
                                "address": "KT1Wkv9KR9jsnp1LLquw9RYtranmB4nCim37"
                            },
                            "value": "0"
                        }
                    },
                    {
                        "bigmap": 9920,
                        "path": "ledger",
                        "action": "add_key",
                        "content": {
                            "hash": "exprtfzRvhFxtjoSrYvuf77SRmAPNnFJdf9ykBYW7uCNJSMaCTASAj",
                            "key": {
                                "nat": "95900",
                                "address": "tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK"
                            },
                            "value": "1"
                        }
                    }
                ],
                "status": "applied",
                "hasInternals": False,
                "tokenTransfersCount": 1
            }
        ],
        "state": 2692112
    }
])"""
print(str([('tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK', 25, 3, None, None, None), ('tz1LK1kJ73YwKEd8xpkCKtACc13qQayrfAeZ', 15, 1, '5%', 'commission', '')]))
print(str(model.eligible()))