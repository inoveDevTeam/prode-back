import os
import sys
import locale

# Primero, importamos los serializadores
#from apuestas.api.serializers import *

# Segundo, importamos los modelos:
from http.client import HTTPResponse
from textwrap import indent
from django.contrib.auth.models import User
from apuestas.models import *

# Importamos librerías para gestionar los permisos de acceso a nuestras APIs
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

# Importamos librerías para seleccionar el tipo de API
from rest_framework.views import APIView

# Importamos librerías para tipo de parser
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Librerías para gestionar los tokens en el login
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from django.utils import timezone


class LoginUserAPIView(APIView):
    '''
    ```
    Vista de API personalizada para recibir peticiones de tipo POST.
    Esquema de entrada:
    {"username":"root", "password":"12345"}
    
    ```
    '''
    parser_classes = (JSONParser,)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        user_data = {}
        try:
            # Obtenemos los datos del request:
            username = request.data.get('username')
            password = request.data.get('password')
            # Obtenemos el objeto del modelo user, a partir del usuario y contraseña,
            # NOTE: es importante el uso de este método, porque aplica el hash del password!
            account = authenticate(username=username, password=password)

            if account:
                # Si el usuario existe y sus credenciales son validas,
                # obtener el TOKEN:
                token, created = Token.objects.get_or_create(user=account)

                # Con todos estos datos, construimos un JSON de respuesta:
                user_data['username'] = username
                user_data['first_name'] = account.first_name
                user_data['last_name'] = account.last_name
                #user_data['is_active'] = account.is_active
                user_data['token'] = token.key                
                # Devolvemos la respuesta personalizada
                return JsonResponse(user_data, status=status.HTTP_201_CREATED)
            else:
                # Si las credenciales son invalidas, devolvemos algun mensaje de error:
                user_data['response'] = 'Error'
                user_data['error_message'] = 'Credenciales invalidas'
                return JsonResponse(user_data, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as error:
            # Si aparece alguna excepción, devolvemos un mensaje de error
            user_data['response'] = 'Error'
            #user_data['error_message'] = error
            return JsonResponse(user_data, status=status.HTTP_400_BAD_REQUEST)


class PartidosPronosticosAPIView(APIView):
    """lista de partidos apostados y no apostados"""
    
    parser_classes = (JSONParser,)

    # HC --> Realizamos directamente el "get", exista o no exista el pronostico
    def get(self, request):
       
        try:  
            # El usuario lo sacamos del request, 
            user = request.user  

            data = []
            
            # Buscar todas los partidos
            datos_partidos = Partido.objects.all().order_by("fecha")

            # Buscar los pronosticos del user
            pronosticos = Pronostico.objects.filter(usuario=user).order_by("partido__fecha")

            locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

            # Recorre los partidos guardados
            for match in datos_partidos:

                if match.cerrado == False and match.terminado == False:
                    estado = 0
                elif match.cerrado == True and match.terminado == False:
                    estado = 1
                else:
                    estado = 2

                dict_partidos = {
                    "partido_id": match.id,
                    "torneo_name": match.torneo.name,
                    "equipo_1": match.equipo_1.name,
                    "equipo_2": match.equipo_2.name,
                    "fecha": timezone.localtime(match.fecha).strftime('%A %d, %B %Y %H:%M'),
                    "descripcion": match.descripcion,
                    "estado": estado,
                    "resultado_equipo_1": match.resultado_equipo_1,
                    "resultado_equipo_2": match.resultado_equipo_2,
                    # Se muestra que no está apostado
                    "pronostico_equipo_1": None,
                    "pronostico_equipo_2": None,
                    "puntaje": 0
                    }

                for pronostico in pronosticos: # Recorre los pronosticos guardados del user
                    partido_forecast = pronostico.partido # Patidos pronosticados por el user

                    if match.id == partido_forecast.id: # Si el nro de partido es igual al partido apostado
                        # Actualiza en los datos los campos apostados por el usuario
                        dict_partidos["pronostico_equipo_1"] = pronostico.pronostico_equipo_1,
                        dict_partidos["pronostico_equipo_2" ] = pronostico.pronostico_equipo_2,
                        dict_partidos["puntaje"] = pronostico.puntaje
                        break

                data.append(dict_partidos)

            return JsonResponse({"data": data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"{fname} {exc_tb.tb_lineno} {e}") # esto lo vamos a mejorar con logging
            # HC --> ya que no retornamos ninguna información de valor,
            # no retornemos ninguna (hay que investigar como mejorar esto)
            return JsonResponse(data={}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        """ Agregar apuesta pronostico_equipo_1 y pronostico_equipo_2 """

        try:
            user = request.user

            partido_id = int(request.data['partido_id'])
            pronostico_equipo_1 = int(request.data['pronostico_equipo_1'])
            pronostico_equipo_2 = int(request.data['pronostico_equipo_2'])
         
            Pronostico.objects.filter(partido=partido_id, usuario=user).update( 
                                                   pronostico_equipo_1=pronostico_equipo_1,
                                                   pronostico_equipo_2=pronostico_equipo_2
                                                   )

           
            return JsonResponse(data={}, status=status.HTTP_200_OK)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"{fname} {exc_tb.tb_lineno} {e}") # esto lo vamos a mejorar con logging
            # HC --> ya que no retornamos ninguna información de valor,
            # no retornemos ninguna (hay que investigar como mejorar esto)
            return JsonResponse(data={}, status=status.HTTP_400_BAD_REQUEST)