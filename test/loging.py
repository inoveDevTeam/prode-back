import json
import requests

url = "http://127.0.0.1:8000/api/v1.0/login/"
data = {"username":"hernan", "password":"prode1234"}

resp = requests.post(url, json=data)
print(resp.status_code)
print(resp.json())