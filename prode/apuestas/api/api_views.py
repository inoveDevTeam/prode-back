# Primero, importamos los serializadores

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


class  PartidosAPIView(APIView):
    """lista de partidos (en cada uno se especifica si se pueda apostar o si ya está terminado)"""
    
    def get(self, request):

        if request.method == 'GET':
            try:          
                # Buscar todas los partidos
                datos = list(Partido.objects.values()) 
                data = {}
                data['data'] = datos 
               
                return JsonResponse(data, status=status.HTTP_201_CREATED)

            except:
                data['response'] = 'Error'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class PronosticosAPIView(APIView):
    
    def get(self, request):

        if request.method == 'GET':
            """ Retorna la lista de mis apuestas(por usuario) con sus puntajes"""
            try:
                datos = list(Pronostico.objects.values()) 
                data = {}
                
                contador = 1
                mis_apuestas = []
                dict_data = []

                for diccionario in datos:
                    for k,v in diccionario.items():
                        
                        dict_data = {"pronostic_equipo_1":diccionario["pronostico_equipo_1"], 
                                "pronostico_equipo_2":diccionario["pronostico_equipo_2"], 
                                "puntaje":diccionario["puntaje"], 
                                "partido_id":diccionario["partido_id"]}
                

                        if diccionario['usuario_id'] == contador:
                            mis_apuestas.append(dict_data)
                            data[f'user_{contador}']= mis_apuestas
                            break

                        else:
                            # Pasa al siguiente usuario y se vacia la lista de apuesta para el siguientes usuario.
                            contador +=1
                            mis_apuestas = []
                            mis_apuestas.append(dict_data)
                            data[f'user_{contador}']= mis_apuestas
                            break
                                       
                return JsonResponse(data, status=status.HTTP_201_CREATED)

            except:
                data['response'] = 'Error'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class PronosticosIdAPIView(APIView): 
    
    def put(self, request, pk, t1, t2):
                
        if request.method == 'PUT':
            """ Modificar apuesta resultado_equipo_1 y resultado_equipo_2 """ #verificar si es resultado o pronostico
            
            try:
                # Busca por id y actualiza los pronosticos
                Pronostico.objects.values().filter(id=pk).update(pronostico_equipo_1 = t1,
                                                                        pronostico_equipo_2 = t2)
                # Verificar si se hizo la actualización
                update = Pronostico.objects.values().filter(id=pk).first()
                data = {}
                data['update'] = update 
                print(data)   

                return Response(data, status=status.HTTP_201_CREATED)
                
            except:
                data['response'] = 'Error'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
    

class PronosticosApustaAPIView(APIView):

    def post(self, request, user, e1, e2, p1, p2, punto):
        """Crear apuesta"""
        data = {}
        print(user, e1, e2, p1, p2, punto)
        if request.method == 'POST':
            try:
                
                # 1Crear usuario con parámetro user
                user_filter=User.objects.values().filter(username=user).exists()
                print(user_filter)
                if user_filter is False:
                    User.objects.create_user(user, password="prode1234")
                
                else: 
                    usuario_reg= User.objects.get(username=user)
                    print(usuario_reg.username)

                # 2Necesito el id
                usuario_reg= User.objects.get(username=user) #Retorna toda la info del usuario como objeto usuario_reg.id
                

                # 3Verificar si los equipos estan registrados
                equipo_filter_1 = Equipo.objects.values().filter(name=e1).exists()
                equipo_filter_2 = Equipo.objects.values().filter(name=e2).exists()
                print(equipo_filter_1, equipo_filter_2)

                if equipo_filter_1 is False and equipo_filter_2 is False:
                    Equipo.objects.create(name=e1)
                    Equipo.objects.create(name=e2)

                if equipo_filter_1 is True and equipo_filter_2 is False:
                    Equipo.objects.create(name=e2)

                elif equipo_filter_1 is False and equipo_filter_2 is True:
                    Equipo.objects.create(name=e1)
                    
                # EQUIPOS YA REGISTRADOS
                equipos = list(Equipo.objects.values())
                #print(equipos)

                equipo_1 =Equipo.objects.filter(name=e1).first() # Retorna objeto y se accede al id --> equipo_1.id
                print(equipo_1.id)
                equipo_2 = Equipo.objects.filter(name=e2).first()  # Retorna objeto y se accede al id --> equipo_2.id
                print(equipo_2.id)
                
                # 4Armar partido
                # Se necesita el nombre del torneo y id 
                copa_age = Torneo.objects.get(name='Copa Age 2020') # Objeto copa_age y se accede al id --> copa_age.id)
                print(copa_age)
                # # verificar si hay partido armado con ambos equipos y si partido_filter is False crea el  partido
                partido_filter=Partido.objects.filter(equipo_1 = equipo_1.id, 
                                                      equipo_2 = equipo_2.id).exists()
              
                print(partido_filter)
                # Sino hay partido lo crea
                if partido_filter is False:
                    
                    Partido.objects.create(
                                        torneo = copa_age,
                                        equipo_1 = equipo_1,
                                        equipo_2 = equipo_2,
                                        fecha = timezone.now(),
                                        resultado_equipo_1 = 0,
                                        resultado_equipo_2 = 0,
                                        )
                    # Se necesita obtener el id del partido
                    # Se buscar el partido recién registrado con los dos equipos objetos, pasados por parámetro partido_new.id  
                    partido = Partido.objects.get(equipo_1=equipo_1.id, equipo_2 = equipo_2.id) 
                    print(partido.id)

                else:
                    partido = Partido.objects.filter(
                                        torneo = copa_age,
                                        equipo_1 = equipo_1,
                                        equipo_2 = equipo_2).first()

                    print('id partido', partido.id)


                #4crear apuesta
                prono_existe =Pronostico.objects.filter(
                                        usuario = usuario_reg, #Objeto completo
                                        partido = partido, #Objeto completo
                                        pronostico_equipo_1 = p1,
                                        pronostico_equipo_2 = p2,
                                        puntaje = punto,
                                    ).exists()

                #print('Existe pronostico?',prono_existe)

                if prono_existe is False:
                    Pronostico.objects.create(
                                            usuario = usuario_reg, #Objeto completo
                                            partido = partido, #Objeto completo
                                            pronostico_equipo_1 = p1,
                                            pronostico_equipo_2 = p2,
                                            puntaje = punto,
                                        )

                    data = Pronostico.objects.values(usuario=usuario_reg, 
                                                    partido = partido,
                                                    pronostico_equipo_1 = p1,
                                                    pronostico_equipo_2 = p2,
                                                    puntaje = punto,).values()
                    

                else:
                    data =Pronostico.objects.filter(
                                        usuario = usuario_reg, #Objeto completo
                                        partido = partido, #Objeto completo
                                        pronostico_equipo_1 = p1,
                                        pronostico_equipo_2 = p2,
                                        puntaje = punto,).values()
                print(data)
                return Response(data, status=status.HTTP_201_CREATED)


            except:
                data['response'] = 'Error'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)