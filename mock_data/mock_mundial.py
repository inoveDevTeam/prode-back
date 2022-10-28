import os
import csv
from apuestas.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


with open("../mock_data/mundial.csv") as fi:
    data = list(csv.DictReader(fi))

admin = User.objects.create_user("admin", password="prode1234", is_staff=True, is_superuser=True)

Configuracion.objects.create(
    name="puntos_ganador",
    value="5",
    descripcion="Puntos asociados a acertar quien gana el partido"
    )

Configuracion.objects.create(
    name="puntos_resultado_exacto",
    value="10",
    descripcion="Puntos asociados a acertar exactamente el resultado"
    )

Configuracion.objects.create(
    name="tiempo_cierre_apuestas",
    value="30",
    descripcion="Hasta cuanto tiempo antes del partido puede apostar los usuarios"
    )


torneo = Torneo.objects.create(name="Qatar 2022")

equipos = []
for row in data:
    equipos.append(row["equipo1"].capitalize())
    equipos.append(row["equipo2"].capitalize())

equipos = sorted(list(set(equipos)))
equipos_db = {}
for equipo in equipos:
    equipos_db[equipo] = Equipo.objects.create(name=equipo)

meses = {"nov": 11, "dic": 12}

for row in data:
    dia = int(row["fecha"].split("-")[0])
    mes = meses[row["fecha"].split("-")[1]]
    hora = int(row["hora"])
    fecha = timezone.make_aware(datetime(2022, mes, dia, hora))
    Partido.objects.create(
        torneo = torneo,
        equipo_1 = equipos_db[row["equipo1"].capitalize()],
        equipo_2 = equipos_db[row["equipo2"].capitalize()],
        fecha = fecha,
        descripcion=f'Grupo {row["grupo"]}'
    )
