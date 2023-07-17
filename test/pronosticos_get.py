import json
import requests

token = "33055a22bc191a9e82e3c122ae3769f5d0a82326"
headers = {
    'Authorization': f'Token {token}',
    "Content-Type": "application/json"
}

url = "http://127.0.0.1:8000/api/v1.0/partidos/pronosticos/"

resp = requests.get(url, headers=headers)
print(resp.status_code)
print(resp.json())