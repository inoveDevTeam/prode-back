from apuestas.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

hernan = User.objects.create_user("hernan", password="prode1234")
johana = User.objects.create_user("johana", password="prode1234")
santiago = User.objects.create_user("santiago", password="prode1234")

copa_age = Torneo.objects.create(name="Copa Age 2020")

equipo_1 = Equipo.objects.create(name="Equipo1")
equipo_2 = Equipo.objects.create(name="Equipo2")
equipo_3 = Equipo.objects.create(name="Equipo3")
equipo_4 = Equipo.objects.create(name="Equipo4")

partido_1 = Partido.objects.create(
        torneo = copa_age,
        equipo_1 = equipo_1,
        equipo_2 = equipo_2,
        fecha = timezone.now(),
        resultado_equipo_1 = 3,
        resultado_equipo_2 = 0,
    )

partido_2 = Partido.objects.create(
        torneo = copa_age,
        equipo_1 = equipo_1,
        equipo_2 = equipo_3,
        fecha = timezone.now(),
        resultado_equipo_1 = 1,
        resultado_equipo_2 = 1,
    )

partido_3 = Partido.objects.create(
        torneo = copa_age,
        equipo_1 = equipo_1,
        equipo_2 = equipo_4,
        fecha = timezone.now(),
        resultado_equipo_1 = 0,
        resultado_equipo_2 = 1,
    )

partido_4 = Partido.objects.create(
        torneo = copa_age,
        equipo_1 = equipo_2,
        equipo_2 = equipo_3,
        fecha = timezone.now(),
        resultado_equipo_1 = 2,
        resultado_equipo_2 = 3,
    )

partido_5 = Partido.objects.create(
        torneo = copa_age,
        equipo_1 = equipo_3,
        equipo_2 = equipo_4,
        fecha = timezone.now(),
        resultado_equipo_1 = 2,
        resultado_equipo_2 = 2,
    )

Pronostico.objects.create(
        usuario = hernan,
        partido = partido_1,
        pronostico_equipo_1 = 3,
        pronostico_equipo_2 = 0,
        puntaje = 15
    )
Pronostico.objects.create(
        usuario = hernan,
        partido = partido_2,
        pronostico_equipo_1 = 0,
        pronostico_equipo_2 = 0,
        puntaje = 10
    )
Pronostico.objects.create(
        usuario = hernan,
        partido = partido_4,
        pronostico_equipo_1 = 1,
        pronostico_equipo_2 = 0,
        puntaje = 0
    )
Pronostico.objects.create(
        usuario = hernan,
        partido = partido_5,
        pronostico_equipo_1 = 2,
        pronostico_equipo_2 = 2,
        puntaje = 15
    )
Pronostico.objects.create(
        usuario = johana,
        partido = partido_1,
        pronostico_equipo_1 = 2,
        pronostico_equipo_2 = 0,
        puntaje = 10
    )