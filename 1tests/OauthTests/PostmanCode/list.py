import requests

url = "https://gmail.googleapis.com/gmail/v1/users/brianplavery@gmail.com/messages"

payload={}
headers = {
  'Authorization': 'Bearer xxx'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)