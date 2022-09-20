from django.db import models
# NOTE: Para poder utilizar el modelo "user" que viene por defecto en Django,
# Debemos importarlo previamente:
from django.contrib.auth.models import User

class Usuario(User):
    username = models.CharField(db_column = 'username', unique = True,
                                max_length = 150, null = False, blank = False,
                                primary_key = True) 
    email = models.EmailField(verbose_name ='correo', unique=True, max_length = 255)
    password = models.CharField(max_length= 20, blank= False, null= False)
    groups = models.CharField(verbose_name ='grupos',max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
    
    def __str__(self):
        return f'{self.username, self.groups}'
    

class Token(models.Model):
    id = models.BigAutoField(db_column = 'ID', primary_key = True)
    username = models.ForeignKey(Usuario) 
    # token = 


class Torneo(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    torneo'''
    
    id = models.BigAutoField(db_column = 'ID', primary_key = True)
    name = models.CharField(deb_column = 'name', max_length = 60, default='')
   
    class Meta:
        db_table = 'torneo'
            
    def __str__(self):
        return f'{self.id, self.name}'


class Equipo(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    equipo'''
    id = models.BigAutoField(db_column = 'ID', primary_key = True)
    name = models.CharField(db_column = 'name', max_length = 60)
   
    class Meta:
        db_table = 'equipo'
            
    def __str__(self):
        return f'{self.name}'


class Partido(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    partido'''

    id = models.BigAutoField(db_column ='ID', primary_key = True)
    torneo = models.ForeignKey(Torneo, verbose_name = 'torneo') 
    equipo_1 = models.ForeignKey(Equipo, verbose_name = 'equipo_1') 
    equipo_2 = models.ForeignKey(Equipo, verbose_name = 'equipo_2') 
    fecha = models.DateTimeField(verbose_name = 'fecha')
    descripcion = models.CharField(verbose_name = 'descripcion', max_length = 60,  default ='')
    cerrado = models.BooleanField(verbose_name = 'cerrado',default = False, blank = True) 
    resultado_equipo_1 = models.PositiveIntegerField(verbose_name = 'resultado_equipo_1',default = None, blank = True)     
    resultado_equipo_2 = models.PositiveIntegerField(verbose_name = 'resultado_equipo_2',default = None, blank = True)
    terminado =  models.BooleanField(verbose_name = 'terminado',default = False, blank = True)

    class Meta:
        db_table = 'partido'
            
    def __str__(self):
        return f'{self.id, self.torneo, self.equipo_1, self.equipo_2, self.resultado_equipo_1, self.resultado_equipo_2}'


class Pronostico(models.Model):
    '''Esta clase hereda de Django models.Model y crea una tabla llamada
    pronostico'''

    id = models.BigAutoField(db_column ='ID', primary_key = True)
    usuario = models.ForeignKey(User, verbose_name = 'usuarios',
                                on_delete = models.DO_NOTHING, default=1, blank=True)  # Hereda de User de djando (ya fue invocado inicialmente)
    partido = models.ForeignKey(Partido, verbose_name = 'partidos') 
    pronostico_equipo_1 = models.PositiveIntegerField(verbose_name = 'pronosticos_equipo_1') 
    pronostico_equipo_2 = models.PositiveIntegerField(verbose_name = 'pronosticos_equipo_2')
    puntaje = models.PositiveIntegerField(verbose_name = 'puntajes')

    class Meta:
        db_table = 'pronostico'
            
    def __str__(self):
        return f'{self.id, self.partido, self.pronostico_equipo_1, self.pronostico_equipo_2, self.puntaje}'