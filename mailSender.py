import requests

url = "https://emailapi.netcorecloud.net/v5/mail/send"
headers = {
 	'api_key': "4a7e335c545f56470e71c4bb33fd0bf8",
 	'content-type': "application/json"
 	}
def sendAlert(objet,alert):
    payload = "{\"from\":{\"email\":\"achillerondo@pepisandbox.com\",\"name\":\"Talao Analytics Alerts\"},\"subject\":\""+objet+"\",\"content\":[{\"type\":\"html\",\"value\":\""+alert+"\"}],\"personalizations\":[{\"to\":[{\"email\":\"achillerondo@gmail.com\",\"name\":\"Lionel Messi\"}]}]}"
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)