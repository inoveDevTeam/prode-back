import json
import requests

token = "c52ec8d3fdbfdaf776b869a41fb7c5de48592c5d"
headers = {
    'Authorization': f'Token {token}',
    "Content-Type": "application/json"
}

url = "http://127.0.0.1:8000/api/v1.0/partidos/pronosticos/"

data = {
    "partido_id": 1,
    "pronostico_equipo_1": 2,
    "pronostico_equipo_2": 2,
}

resp = requests.post(url, json=data, headers=headers)
print(resp.status_code)
print(resp.json())