import requests

authorize_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://oauth2.googleapis.com/token'

payload = {
        'client_id': 52454011030-ll74s70nl503pvclukgepf26ojbo9u1m.apps.googleusercontent.com
        'response_type': 'code',
        'redirect_uri': 'https://ide-e7e7d3b5bdc5401f9c4ac3c950202c63-8080.cs50.xyz',
        'response_mode': 'form_post',
        'scope': 'https://www.googleapis.com/auth/gmail.modify',
        'state': 'foobar'
        }

r = requests.get(authorize_url, params=payload)
print(r.status_code)
print(r.text)