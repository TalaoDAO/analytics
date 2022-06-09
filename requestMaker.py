import requests

params = {"key": "SECRET_KEY"}
body = {
    "@context": [
        "https://www.w3.org/2018/credentials/v1",
        {
            "name" : "https://schema.org/name",
            "description" : "https://schema.org/description",
            "TezVoucher_1" : {
                "@id": "https://github.com/TalaoDAO/context/blob/main/README.md",
                "@context": {
                    "@version": 1.1,
                    "@protected": True,
                    "schema" : "https://schema.org/",
                    "id": "@id",
                    "type": "@type",
                    "associatedAddress" : {
                        "@id": "https://schema.org/address",
                        "@context" : {
                            "@protected" : True,
                            "blockchainTezos" : "https://schema.org/blockchain",
                            "blockchainEthereum" : "https://schema.org/blockchain"
                        }
                    },
                    "affiliate" : {
                        "@id" : "https://github.com/TalaoDAO/context/blob/main/README.md",
                        "@context" : {
                            "@version": 1.1,
                            "@protected": True,
                            "name" : "schema:name",
                            "did" : "schema:identifier",
                            "email" : "schema:email",
                            "phone" : "schema:telephone",
                            "pseudo" : "schema:givenName",
                            "benefit" : {
                                "@id" : "https://github.com/TalaoDAO/context/blob/main/README",
                                "@context" : {
                                    "price" : "schema:value",
                                    "category" : "schema:category",
                                    "incentiveCompensation" : "schema:incentiveCompensation"
                                }
                            },
                            "paymentAccepted" : {
                                "@id" : "schema:paymentAccepted",
                                "@context" : {
                                    "blockchain" : "schema:name",
                                    "currency" : "schema:currency",
                                    "blockchainAccount" : "schema:identifier"
                                }
                            }
                        }
                    },
                    "offers" : {
                        "@id" : "schema:offer",
                        "@context" : {
                            "@version": 1.1,
                            "@protected": True,
                            "startDate" : "schema:date",
                            "category" : "schema:category",
                            "duration" : "schema:duration",
                            "endDate" : "schema:date",
                            "benefit" : {
                                "@id" : "https://github.com/TalaoDAO/context/blob/main/README",
                                "@context" : {
                                    "price" : "schema:value",
                                    "category" : "schema:category",
                                    "discount" : "schema:discount"
                                }
                            },
                            "offeredBy" : {
                                "@id" : "schema:offeredBy",
                                "@context" : {
                                    "@version": 1.1,
                                    "@protected": True,
                                    "description" : "schema:description",
                                    "website" : "schema:website",
                                    "logo": {"@id" : "schema:image", "@type" : "@id"},
                                    "did" : "schema:identifier",
                                    "name" : "schema:name",
                                    "paymentMethod" : {
                                        "@id" : "schema:paymentMethod",
                                        "@context" : {
                                            "currency" : "schema:currency",
                                            "blockchain" : "schema:name",
                                            "blockchainAccount" : "schema:identifier"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "issuedBy" : {
                        "@id" : "schema:issuedBy",
                        "@context" : {
                            "@version": 1.1,
                            "@protected": True,
                            "website" : "schema:website",
                            "logo": {"@id" : "schema:image", "@type" : "@id"},
                            "did" : "schema:identifier",
                            "name" : "schema:name",
                            "paymentAccepted" : {
                                "@id" : "schema:paymentMethod",
                                "@context" : {
                                    "currency" : "schema:currency",
                                    "blockchain" : "schema:name",
                                    "blockchainAccount" : "schema:identifier"
                                }
                            },
                            "paymentMethod" : {
                                "@id" : "schema:paymentMethod",
                                "@context" : {
                                    "currency" : "schema:currency",
                                    "blockchain" : "schema:name",
                                    "blockchainAccount" : "schema:identifier"
                                } 
                            }
                        }
                    }
                }
            }
        }
    ],
    "id": "urn:uuid:random",
    "type": ["VerifiableCredential", "TezVoucher_1"],
    "issuer": "did:tz:issuer",
    "name" : [ 
        {
            "@value": "5% off Tezotopia NFTs",
            "@language": "en"
        },
        {
            "@value": "5% off Tezotopia NFTs",
            "@language": "de"
        },
        {
            "@value": "5% de reduction sur les NFT Tezotopia",
            "@language": "fr"
        }
    ],
    "description" : [
        {
            "@language": "en",
            "@value": "Get a 5% discount on your first Tezotop Block ! "
        },
        {
            "@language": "de",
            "@value": "Erhalten Sie 5 % Rabatt auf Ihren ersten Tezotop-Block!"
        },
        {
            "@language": "fr",
            "@value": "Bénéficiez de 5% de réduction sur votre premier Bloc Tezotop ! "
        }
    ],
    "credentialSubject" : {
        "id" : "did:wallet",
        "type" : "TezVoucher_1",
        "associatedAddress" : {
                "blockchainTezos" : "tz1345765476547654",
                "blockchainEthereum" : "0x1345765476547654"
        },
        "offers" : [{
            "startDate" : "2022-04-08T19:55:00Z",
            "endDate" : "2022-06-08T19:55:00Z",
            "category" : "discounted_coupon",
            "duration" : "30",
            "benefit" : {
                "category" : "discount",
                "discount" : "5%"
            },    
            "offeredBy": {
                "logo": "ipfs://QmZmdndUVRoxiVhUnjGrKnNPn8ah3jT8fxTCLMnAzRAFFZ",
                "name": "GifGames",
                "description" : "gaming platform Tezotopia",
                "paymentMethod" : {
                    "blockchain" : "Tezos",
                    "currency" : "XTZ",
                    "blockchainAccount" : "tz1iyjrTUNxDpPaqNZ84ipGELAcTWYg66789"
                }
            }
        }],
        "issuedBy": {
            "logo": "ipfs://QmZmdndUVRoxiVhUnjGrKnNPn8ah3jT8fxTCLMnAzRAFFZ",
            "name": "Talao",
            "paymentAccepted" : {
                "blockchain" : "Tezos",
                "currency" : "XTZ",
                "blockchainAccount" : "tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg6s5Du"
            },
            "paymentMethod" : {
                "blockchain" : "Tezos",
                "currency" : "XTZ",
                "blockchainAccount" : "tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg6s5Du"
            }
        },
        "affiliate": {
            "name": "to be filled or removed",
            "email" : "to be filled or removed",
            "phone" : "to be filled or removed",
            "pseudo" : "to be filled or removed",
            "paymentAccepted" : {
                "blockchain" : "Tezos",
                "currency" : "XTZ",
                "blockchainAccount" : "tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg5555"
            },
            "benefit" : {
                "category" : "commission",
                "incentiveCompensation" : "2%"
            }   
        }
    }
}


response = requests.post(
    "http://192.168.1.17:3000/analytics/api/newvoucher", json=body, headers=params)
print(response.status_code)
