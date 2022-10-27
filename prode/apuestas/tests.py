from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
# ---
from .models import *

from django.urls import reverse

class TestLoginAPIViewTestCase(APITestCase):
    
    def setUp(self):
        '''Inicialización de la clase'''

        self.url = reverse('login')
        self.url2 = reverse('partidos')

        # Se crea el usuario
        self.user = User.objects.create_user(
                        username="test", 
                        password="prode1234"
                        )
        return super().setUp()

    def test_login(self):
        response = self.client.post(
        self.url,
            {
                'username':"test",
                'password':"prode1234"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # El código de respuesta cuando se crea un user es 201

        # Tomar el token para un proximo request        
        print(response.json())
        token = response.json()["token"]

        # Utilizar el token para autenticarnos
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Relealizar una nueva peticion
        response = self.client.get(
            path=self.url2,
            data={
                'username':"test",
                'password':"prode1234"
            },
            format='json',
        )
        print(response.json())


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


  
  
