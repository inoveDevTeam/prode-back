from django.test import TestCase
from apuestas import models
from django.contrib.auth.models import User
from django.test import Client

# Create your tests here.

class MiClaseDePrueba(TestCase):
    '''Clase de prueba para hacer Unit Test sobre los modelos de la base de datos.'''

    usuario = "Luna"
    partido = 4
    pronostico_equipo_1 = 2
    pronostico_equipo_2 = 0
    puntaje = 0

    '''Aquí configuramos las condiciones de la prueba, por lo general insertamos a la DB'''
    
    def setUp(self):
        pronostico = models.Pronostico.objects.create(
            id = 18,
            usuario = self.usuario,
            partido = self.partido,
            pronostico_equipo_1 = self.pronostico_equipo_1,
            pronostico_equipo_2 = self.pronostico_equipo_2,
            puntaje = self.puntaje,
        )

    def test_pruebas_de_integridad_de_datos(self):
        '''
        Este método realiza la prueba de integridad de los dato insertados en la base de datos, 
        aprovechando "self.atributo" para verificarlos. 
        '''
        # Llamamos al objeto seteado:
        pronostico = models.Pronostico.objects.get(id=18)

        # Extraemos sus atributos:
        usuario = pronostico.usuario,
        partido = pronostico.partido,
        pronostico_equipo_1 = pronostico.pronostico_equipo_1,
        pronostico_equipo_2 = pronostico.pronostico_equipo_2,
        puntaje = pronostico.puntaje

        # Generamos dos listas para compararlas, una con los datos extraidos del modelo
        # y otra con los datos que fueron insertados en el modelo
        object_values = [usuario, partido, pronostico_equipo_1, pronostico_equipo_2, puntaje]

        test_values = [self.usuario, self.partido,
                       self.pronostico_equipo_1, self.pronostico_equipo_2, self.puntaje]

        # Comparamos uno a uno los datos:
        for index in range(len(test_values)):
            print(object_values[index], test_values[index])

            if object_values[index] != test_values[index]:
                # Si los datos son distintos, hacemos que la prueba de fallida:
                self.assertEqual(object_values[index], test_values[index])
                
        # Si los datos son iguales, verificamos que las pruebas son exitosas:
        self.assertTrue(True)



class PruebaDeAPIs(TestCase):
    '''
    Test para las APIs del sistema, utilizaremos una DB y un server de prueba.
    '''
    # NOTE: Configuramos los atributos de la clase para utilizarlos en todos los métodos:
    username = 'root'
    password = '12345'
    email = 'algo@algo.com'
    user = None
    pronostico = None

    # Client() es un objeto que gestiona la conexión con los endpoints, como lo haría un request
    client = Client()

    def setUp(self):
        '''
        Aquí configuramos las condiciones de la prueba, 
        creamos un pronostico y generamos la conexión al server de prueba
        NOTE: Aquí debemos crear los objetos para la base de datos de prueba, 
        de lo contrario, se insertarán en la base de datos del sistema.
        '''

        # NOTE: Creamos un superusuario para las pruebas:
        self.user = User.objects.create_superuser(self.username, self.email, self.password)

        # Ahora lo autenticamos en el servidor de pruebas:
        self.client.login(username=self.username, password=self.password)

        # Insertamos un pronostico en la DB de prueba:
        self.pronostico = models.Pronostico.objects.create(
            id = 3,
            usuario = "Martes",
            partido = 8,
            pronostico_equipo_1 = 2,
            pronostico_equipo_2 = 2,
            puntaje = 0
        )

    def test_api_partidos_pronosticos(self):
        '''
        Test de endpoint: partidos/pronosticos/
        Pruebas sobre todos los métodos.
        '''

        # Preparamos los datos:
        endpoint = '/partidos/pronosticos/'
        data = {
            'id': 4,
            'usuario': 'Martes',
            'partido': 8,
            'pronostico_equipo_1': 2,
            'pronostico_equipo_2': 2,
            'puntaje': 0
        }

        # GET test:
        resp = self.client.get(endpoint)
        self.assertEqual(resp.status_code, 200) 

        # POST test:
        resp = self.client.post(
            endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 201)


  
  
