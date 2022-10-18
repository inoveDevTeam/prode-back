from django.db import models
# NOTE: Para poder utilizar el modelo "user" que viene por defecto en Django,
# Debemos importarlo previamente:
from django.contrib.auth.models import User

class Configuracion(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    configuracion'''

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=60, default='')
    value = models.CharField(max_length=60, default='')
    descripcion = models.CharField(max_length=150, default='', blank=True)
   
    class Meta:
        db_table = 'configuracion'


class Torneo(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    torneo'''

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=60, default='')
   
    class Meta:
        db_table = 'torneo'
            
    def __str__(self):
        return f'{self.name}'


class Equipo(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    equipo'''

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=60)
   
    class Meta:
        db_table = 'equipo'
            
    def __str__(self):
        return f'{self.name}'


class Partido(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    partido'''

    id = models.BigAutoField(primary_key=True)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    equipo_1 = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo1_set')
    equipo_2 = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo2_set')
    fecha = models.DateTimeField()
    descripcion = models.CharField(max_length=60, default='', blank=True)
    cerrado = models.BooleanField(default=False, blank=True)
    resultado_equipo_1 = models.PositiveIntegerField(default=None, blank=True, null=True)
    resultado_equipo_2 = models.PositiveIntegerField(default=None, blank=True, null=True)
    terminado =  models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        # Verificar si hay que calcular el puntaje
        # (si el partido ha terminado)
        if self.terminado == True:
            puntos_resultado_exacto = int(Configuracion.objects.get(name="puntos_resultado_exacto").value)
            puntos_ganador = int(Configuracion.objects.get(name="puntos_ganador").value)
            # Resultado del partido
            resultado_equipo_1 = self.resultado_equipo_1
            resultado_equipo_2 = self.resultado_equipo_2

            # Buscar todos las apuestas hechas sobre este partido
            # y computar el puntaje
            pronosticos = Pronostico.objects.filter(partido__id=self.id)
            for p in pronosticos:
                pronostico_equipo_1 = p.pronostico_equipo_1
                pronostico_equipo_2 = p.pronostico_equipo_2
                puntaje = 0

                # Calcular el puntaje
                resultado = resultado_equipo_2 - resultado_equipo_1
                pronostico = pronostico_equipo_2 - pronostico_equipo_1
                
                # Verifica que el pronóstico fue exacto
                if pronostico_equipo_2 == resultado_equipo_2 and resultado_equipo_1 == pronostico_equipo_1:
                    puntaje += (puntos_ganador + puntos_resultado_exacto) 

                # Verifica si hubo empate, donde el usuario predijo el empate pero no la puntuación exacta.
                elif resultado_equipo_1 == resultado_equipo_2 and pronostico_equipo_2 == pronostico_equipo_1 and resultado_equipo_1 != pronostico_equipo_1:
                    puntaje += puntos_ganador
 
                else:
                    # Sino hubo empate, capaz la persona predijo bien quien ganó. Para eso basta con saber si
                    # resultado y pronostico tienen el mismo signo
                    if (resultado * pronostico) > 0:
                        # Si ambos predijeron que el mismo equipo gana, esto tiene que dar positivo
                        puntaje += puntos_ganador

                
                # Almacenamos el puntaje calculado
                p.puntaje = puntaje
                p.save()


        # Guardar los cambios
        self.cerrado = True  # cerramos el partido si ha terminado
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'partido'
            
    def __str__(self):
        return f'{self.id} {self.fecha} {self.equipo_1} {self.equipo_2} resultado: {self.resultado_equipo_1} / {self.resultado_equipo_2}'


class Pronostico(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    pronostico'''

    id = models.BigAutoField(primary_key = True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    pronostico_equipo_1 = models.PositiveIntegerField()
    pronostico_equipo_2 = models.PositiveIntegerField()
    puntaje = models.PositiveIntegerField()

    class Meta:
        db_table = 'pronostico'
            
    def __str__(self):
        return f'id: {self.id} fecha: {self.partido.fecha} {self.usuario.username} apuesta: {self.pronostico_equipo_1} / {self.pronostico_equipo_2} puntaje:{self.puntaje}'
