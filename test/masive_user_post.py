import json
import requests
import csv

token = "e03b46bc03ec2125e4bdf053fe7d66ca5a0613b9"
headers = {
    'Authorization': f'Token {token}',
    "Content-Type": "application/json"
}

url = "http://69.46.1.38:8071/api/v1.0/user/"

with open("prode_morado_2.csv") as fi:
    datos = csv.DictReader(fi)
    for row in datos:
        data = {
            "username": row["Nombre de usuario"],
            "password": row["Password"],
            "email": row["Correo electrónico"],
            "first_name": row["Nombre/s"],
            "last_name": row["Apellido/s"],
        }
        #print(data)

        resp = requests.post(url, json=data, headers=headers)
        #print(resp.status_code)
        if resp.ok == False:
            print(resp.json())