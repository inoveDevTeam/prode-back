# Primero, importamos los serializadores

# Segundo, importamos los modelos:
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
