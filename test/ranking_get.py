import json
import requests

token = "fab4ab8966f39247e0718353ea8acca96e4ad7c2"
headers = {
    'Authorization': f'Token {token}',
    "Content-Type": "application/json"
}

url = "http://127.0.0.1:8000/api/v1.0/ranking/"

resp = requests.get(url, headers=headers)
print(resp.status_code)
print(resp.json())