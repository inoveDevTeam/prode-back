import os
import csv
from apuestas.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


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


torneo = Torneo.objects.create(name="Wololo 2022")

equipos = [
    "Theviper",
    "Liereyy",
    "Yo",
    "Daut",
    "Vinchester",
    "Villese",
    "Hera",
    "Tatoh",
    "Jordan",
    "Mbl",
    "Accm",
    "Nicov",
    "Sitaux",
    "Capoch",
    "Valas",
    "Daniel"
]


equipos = sorted(list(set(equipos)))
equipos_db = {}
for equipo in equipos:
    equipos_db[equipo] = Equipo.objects.create(name=equipo)

