import requests
import json
url = "http://192.168.1.17:3000/analytics/api/newvoucher"
headers = {
    "key" : "SECRET_KEY",
    "Content-Type": "application/x-www-form-urlencoded",
    }
data = {"voucher" : {"exemple":"my_voucher"}}
print(type(data))
print("-----------------"+data["voucher"]["exemple"])
r = requests.post(url, data=json.dumps(data), headers=headers)
print(r.text)
if not 199<r.status_code<300 :
    print("API call rejected %s", r.status_code)
else :
    print("API call accepted %s", r.status_code)