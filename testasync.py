from flask import Flask, render_template, request, redirect, url_for, render_template_string, jsonify, request, Response
from flask_qrcode import QRcode
from datetime import timedelta
import didkit
import redis
import socket
import uuid
import json
import sys
import sqlite3 as sql
import asyncio
async def main():
    print('hello')
    await didkit.verify_presentation('{"@context":["https://www.w3.org/2018/credentials/v1"],"id":"urn:uuid:f82177f0-963b-41d1-ae13-0249c61c0103","type":["VerifiablePresentation"],"verifiableCredential":{"@context":["https://www.w3.org/2018/credentials/v1",{"walletNotation":"https://schema.org/notation","offers":{"@context":{"@protected":true,"@version":1.1,"benefit":{"@context":{"category":"schema:category","discount":"schema:discount","price":"schema:value"},"@id":"https://github.com/TalaoDAO/context/blob/main/README"},"category":"schema:category","endDate":"schema:date","offeredBy":{"@context":{"@protected":true,"@version":1.1,"description":"schema:description","did":"schema:identifier","logo":{"@id":"schema:image","@type":"@id"},"name":"schema:name","paymentMethod":{"@context":{"blockchain":"schema:name","blockchainAccount":"schema:identifier","currency":"schema:currency"},"@id":"schema:paymentMethod"},"website":"schema:website"},"@id":"schema:offeredBy"},"startDate":"schema:date"},"@id":"schema:offer"},"associatedAddress":{"@context":{"@protected":true,"blockchain":"https://schema.org/blockchain","blockchainAccount":"https://schema.org/address"},"@id":"https://schema.org/address"},"affiliate":{"@context":{"@protected":true,"@version":1.1,"benefit":{"@context":{"category":"schema:category","incentiveCompensation":"schema:incentiveCompensation","price":"schema:value"},"@id":"https://github.com/TalaoDAO/context/blob/main/README"},"did":"schema:identifier","email":"schema:email","name":"schema:name","paymentAccepted":{"@context":{"blockchain":"schema:name","blockchainAccount":"schema:identifier","currency":"schema:currency"},"@id":"schema:paymentAccepted"}},"@id":"https://github.com/TalaoDAO/context/blob/main/README.md"},"talaoAccount":"https://schema.org/account"}],"id":"did:tz2:....","type":["VerifiableCredential","TalaoCommunity"],"credentialSubject":{"id":"did:tz:tz2DHsghAAqFH1wxu5zrU7my5dWMZMzqNT3B","talaoAccount":"0x83E0481C1844Ed257efE1147218C125832F10236","affiliate":{"benefit":{"category":"commission","incentiveCompensation":"5%"},"email":"contact@talao.co","name":"Talao","paymentAccepted":{"blockchain":"Tezos","blockchainAccount":"tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg5555","currency":"XTZ"}},"walletNotation":"Gold","type":"TalaoCommunity","offers":[{"benefit":{"category":"discount","discount":"15%"},"category":"discounted_coupon","endDate":"2022-06-08T19:55:00Z","offeredBy":{"description":"gaming platform Tezotopia","logo":"ipfs://QmZmdndUVRoxiVhUnjGrKnNPn8ah3jT8fxTCLMnAzRAFFZ","name":"GifGames","paymentMethod":{"blockchain":"Tezos","blockchainAccount":"tz1iyjrTUNxDpPaqNZ84ipGELAcTWYg66789","currency":"XTZ"}},"startDate":"2022-04-08T19:55:00Z"}],"associatedAddress":[{"blockchain":"tezos","blockchainAccount":"tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"},{"blockchain":"ethereum","blockchainAccount":"0x461B99bCBdaD9697d299FDFe0879eC04De256DA1"},{"blockchain":"polygon","blockchainAccount":"0x461B99bCBdaD9697d299FDFe0879eC04De256DA1"}]},"issuer":"did:tz:tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg6s5Du","issuanceDate":"2022-05-18T09:15:29Z","proof":{"@context":{"Ed25519BLAKE2BDigestSize20Base58CheckEncodedSignature2021":{"@context":{"@protected":true,"@version":1.1,"challenge":"https://w3id.org/security#challenge","created":{"@id":"http://purl.org/dc/terms/created","@type":"http://www.w3.org/2001/XMLSchema#dateTime"},"domain":"https://w3id.org/security#domain","expires":{"@id":"https://w3id.org/security#expiration","@type":"http://www.w3.org/2001/XMLSchema#dateTime"},"id":"@id","jws":"https://w3id.org/security#jws","nonce":"https://w3id.org/security#nonce","proofPurpose":{"@context":{"@protected":true,"@version":1.1,"assertionMethod":{"@container":"@set","@id":"https://w3id.org/security#assertionMethod","@type":"@id"},"authentication":{"@container":"@set","@id":"https://w3id.org/security#authenticationMethod","@type":"@id"},"id":"@id","type":"@type"},"@id":"https://w3id.org/security#proofPurpose","@type":"@vocab"},"publicKeyJwk":{"@id":"https://w3id.org/security#publicKeyJwk","@type":"@json"},"type":"@type","verificationMethod":{"@id":"https://w3id.org/security#verificationMethod","@type":"@id"}},"@id":"https://w3id.org/security#Ed25519BLAKE2BDigestSize20Base58CheckEncodedSignature2021"},"Ed25519PublicKeyBLAKE2BDigestSize20Base58CheckEncoded2021":{"@id":"https://w3id.org/security#Ed25519PublicKeyBLAKE2BDigestSize20Base58CheckEncoded2021"},"P256BLAKE2BDigestSize20Base58CheckEncodedSignature2021":{"@context":{"@protected":true,"@version":1.1,"challenge":"https://w3id.org/security#challenge","created":{"@id":"http://purl.org/dc/terms/created","@type":"http://www.w3.org/2001/XMLSchema#dateTime"},"domain":"https://w3id.org/security#domain","expires":{"@id":"https://w3id.org/security#expiration","@type":"http://www.w3.org/2001/XMLSchema#dateTime"},"id":"@id","jws":"https://w3id.org/security#jws","nonce":"https://w3id.org/security#nonce","proofPurpose":{"@context":{"@protected":true,"@version":1.1,"assertionMethod":{"@container":"@set","@id":"https://w3id.org/security#assertionMethod","@type":"@id"},"authentication":{"@container":"@set","@id":"https://w3id.org/security#authenticationMethod","@type":"@id"},"id":"@id","type":"@type"},"@id":"https://w3id.org/security#proofPurpose","@type":"@vocab"},"publicKeyJwk":{"@id":"https://w3id.org/security#publicKeyJwk","@type":"@json"},"type":"@type","verificationMethod":{"@id":"https://w3id.org/security#verificationMethod","@type":"@id"}},"@id":"https://w3id.org/security#P256BLAKE2BDigestSize20Base58CheckEncodedSignature2021"},"P256PublicKeyBLAKE2BDigestSize20Base58CheckEncoded2021":{"@id":"https://w3id.org/security#P256PublicKeyBLAKE2BDigestSize20Base58CheckEncoded2021"}},"type":"Ed25519BLAKE2BDigestSize20Base58CheckEncodedSignature2021","proofPurpose":"assertionMethod","verificationMethod":"did:tz:tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg6s5Du#blockchainAccountId","created":"2022-05-18T09:15:43.622Z","jws":"eyJhbGciOiJFZERTQSIsImNyaXQiOlsiYjY0Il0sImI2NCI6ZmFsc2V9..BvLwXBw2ZPEdxFd8Yyxa2rklWcdN-nZRPLgS0hy99k8EQMmM-F02zXOi22c2nvg-ppT-lZGg3siHPUuBh0yUCQ","publicKeyJwk":{"crv":"Ed25519","kty":"OKP","x":"FUoLewH4w4-KdaPH2cjZbL--CKYxQRWR05Yd_bIbhQo"}}},"proof":{"@context":["https://identity.foundation/EcdsaSecp256k1RecoverySignature2020/lds-ecdsa-secp256k1-recovery2020-0.0.jsonld","https://demo.spruceid.com/EcdsaSecp256k1RecoverySignature2020/esrs2020-extra-0.0.jsonld"],"type":"EcdsaSecp256k1RecoverySignature2020","proofPurpose":"authentication","challenge":"a88f55f7-da62-11ec-9f6c-e35d4952c89d","verificationMethod":"did:tz:tz2DHsghAAqFH1wxu5zrU7my5dWMZMzqNT3B#blockchainAccountId","created":"2022-05-23T06:38:25.109Z","domain":"http://192.168.1.17","jws":"eyJhbGciOiJFUzI1NkstUiIsImNyaXQiOlsiYjY0Il0sImI2NCI6ZmFsc2V9..G4TFVnsSZECZXT7VqroFZdceGDRgSBn_nBf16dXdB48k20mra_bfSoLpITJAPN_-H0fX9Zu46rOgVbagv794VQE"},"holder":"did:tz:tz2DHsghAAqFH1wxu5zrU7my5dWMZMzqNT3B"}', '{}')
    print('world')
asyncio.run(main())