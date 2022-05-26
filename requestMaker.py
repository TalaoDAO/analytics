import requests

params = {"key": "SECRET_KEY"}
body = {"adressUser": "tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im",
        "expiration": "2022-12-12",
        "discount": 5,
        "benefitAffiliate": 1,
        "benefitAffiliateType": "pourcentage",
        "affiliate": "tz1P3zm6rgzfYM3xHLv4xm9bQbQ5A74oid39"}
response = requests.post(
    "http://192.168.1.17:3000/api/newvoucher", params=body, headers=params)
print(response.status_code)
