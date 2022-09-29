import json
import requests

token = "ce8aec0a47ee26b03f2fe7f4038ba392bba95ed9"
headers = {
    'Authorization': f'Token {token}',
    "Content-Type": "application/json"
}

url = "http://127.0.0.1:8000/api/v1.0/pronosticos/"

data = {
    "partido_id": 1,
    "pronostico_equipo_1": 2,
    "pronostico_equipo_2": 2,
}

resp = requests.post(url, json=data, headers=headers)
print(resp.status_code)
print(resp.json())