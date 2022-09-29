import json
import requests

token = "ce8aec0a47ee26b03f2fe7f4038ba392bba95ed9"
headers = {
    'Authorization': f'Token {token}',
    "Content-Type": "application/json"
}

url = "http://127.0.0.1:8000/api/v1.0/partidos/"

resp = requests.get(url, headers=headers)
print(resp.status_code)
print(resp.json())