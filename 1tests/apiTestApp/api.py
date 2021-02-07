import requests

url_countries = "https://restcountries.eu/rest/v2/all"
url_currencies = "https://api.coinbase.com/v2/currencies"

countries = requests.get(url_countries).json()
currencies = requests.get(url_currencies).json()

print(len(countries))

#for i in range(len(countries)):
#    print(countries[i]['name'])