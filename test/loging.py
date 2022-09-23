import json
import requests

url = "http://127.0.0.1:8000/api/v1.0/login/"
data = {"username":"hernan", "password":"1234prode"}

resp = requests.post(url, json=data).json()
print(resp)