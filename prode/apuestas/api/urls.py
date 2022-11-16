from django.urls import path
from .api_views import *


urlpatterns = [
    path(f'login/', LoginUserAPIView.as_view(), name="login"),
    path(f'partidos/pronosticos/', PartidosPronosticosAPIView.as_view(), name="partidos"),
    path(f'ranking/', RankingAPIView.as_view(), name="ranking"),
    path(f'user/', UserAPIView.as_view(), name="user"),
]
