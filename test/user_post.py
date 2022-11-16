import json
import requests

token = "636cafc282bb944d4af9a7ea428252aa0b94ab7c"
headers = {
    'Authorization': f'Token {token}',
    "Content-Type": "application/json"
}

url = "http://127.0.0.1:8000/api/v1.0/user/"

data = {
    "username": "hernanc",
    "password": "prode1234",
    "email": "hcontigiani.inove@gmail.com",
    "first_name": "Hernan",
    "last_name": "Contigiani",
}

resp = requests.post(url, json=data, headers=headers)
print(resp.status_code)
print(resp.json())