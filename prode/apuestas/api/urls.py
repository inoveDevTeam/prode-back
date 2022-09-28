from django.urls import path
from .api_views import *


urlpatterns = [
    path(f'login/', LoginUserAPIView.as_view(), name="login"),
    path(f'partidos/', PartidosAPIView.as_view(), name="partidos"),
    path(f'pronosticos/', PronosticosAPIView.as_view(), name="pronosticos"),
    path(f'pronosticos/<int:pk>/<int:t1>/<int:t2>/', PronosticosIdAPIView.as_view(), name="actualizar"),
    path(f'pronosticos/<user>/<e1>/<e2>/<int:p1>/<int:p2>/<int:punto>/', PronosticosApustaAPIView.as_view(), name="apuesta"),


]
