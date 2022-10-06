from django.contrib import admin

from apuestas.models import *

# Register your models here.
@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    # Campos en la tabla de registros
    list_display = ('name', 'value', 'descripcion')


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    # Campos en la tabla de registros
    list_display = ('id', 'name')


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    # Campos en la tabla de registros
    list_display = ('id', 'name') 


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    # Campos en la tabla de registros
    list_display = ('id', 'fecha', 
        'equipo_1', 'equipo_2', 
        'resultado_equipo_1', 'resultado_equipo_2', 
        'cerrado', 'terminado')

    # Filtro lateral de elementos:
    list_filter= ('torneo', 'cerrado', 'terminado')


@admin.register(Pronostico)
class PronosticoAdmin(admin.ModelAdmin):
    # Campos en la tabla de registros
    list_display = ('partido_id', 'fecha', 'usuario',
        'pronostico_equipo_1', 'pronostico_equipo_2', 
        'puntaje')

    def partido_id(self, obj):
        return obj.partido.id

    def fecha(self, obj):
        return obj.partido.fecha
