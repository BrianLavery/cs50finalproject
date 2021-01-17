import requests

url = "https://gmail.googleapis.com/gmail/v1/users/brianplavery@gmail.com/messages"

payload={}
headers = {
  'Authorization': 'Bearer ya29.a0AfH6SMDTIX5Kvbc2dlw3AhNo6AD3gBIsFVT_7nHg077K_hLEI1pEnz2a-cothA2wN1TjRX4csPukwKe1oZEOecyrv92JCRExx1xTiPPG51uF6YGa-VoVt4imGynbLS529yaEASjL0Zq17OneXuyHEIssf9iaUw4wG5m7_xxv6ZE'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)