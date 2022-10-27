from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
# ---
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *
# from django.test import Client

  

class TestLoginAPIViewTestCase(APITestCase):
    
    def setUp(self):
        '''Inicialización de la clase'''

        # La ruta de login (tambien se puede usar revere())
        self.login_url = '/login/'

        # Se crea el usuario
        self.user = User(
                        username="test", 
                        password="prode1234"
                        )
        self.user.save()

        # Para realizar las peticiones, viene incorporada el apitestcase y no hay que definirla
        # post recibe la ruta, la data que se le va a enviar y el formato
        response = self.client.post(
            self.login_url,
            {
                'username':"test",
                'password':"prode1234"
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # El código de respuesta cuando se crea un user es 201
        
        #self.token = response.data['token'] # sino funciona usar user_data en vez de data
        # A esta instancia setear la autorización con el token
        #self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        return super().setUp()

    def test_login(self):
        pass
        # print(self.token)



# class TestAPIViewTestCase(APITestCase):
        
#     # nombre = 'test'
#     # password = '12345'
#     partido = 3
#     pronostico_equipo_1 = 2,
#     pronostico_equipo_2 = 2,
#     puntaje = 0
#     user = User(username='test', password='prode1234')
#     user.save()

#     def setUp(self):
#         self.login_url = '/partidos/pronosticos'
            
#         # Creamos un superusuario para las pruebas:
#         #self.user = User.objects.create_superuser(self.nombre, self.password)

#         # Ahora lo autenticamos en el servidor de pruebas:
#         self.client.login(username=self.user.username, password=self.user.password)

#         # Insertamos un pronostico en la DB de prueba:
#         self.pronostico = Pronostico.objects.create(
#             usuario = self.user.username,
#             partido = self.partido,
#             pronostico_equipo_1 = self.pronostico_equipo_1,
#             pronostico_equipo_2 = self.pronostico_equipo_2,
#             puntaje = self.puntaje
#         )

#     def test_api_partidos_pronosticos(self):
#         '''
#         Test de endpoint: partidos/pronosticos/
#         Pruebas sobre todos los métodos.
#         '''

#         # Preparamos los datos:
#         endpoint = '/partidos/pronosticos/'
#         data = {
#             'usuario': self.user.username,
#             'partido': self.partido,
#             'pronostico_equipo_1': self.pronostico_equipo_1,
#             'pronostico_equipo_2': self.pronostico_equipo_2,
#             'puntaje': self.puntaje
#         }

#         # GET test:
#         resp = self.client.get(endpoint)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK) 

#         # POST test:
#         resp = self.client.post(
#             endpoint, data, content_type="application/json")
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)


  
  
