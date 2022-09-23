from django.urls import path
from .api_views import *


urlpatterns = [
    path(f'login/', LoginUserAPIView.as_view(), name="login"),

]