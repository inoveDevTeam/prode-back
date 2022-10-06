from django.urls import path, include


urlpatterns = [
    path('api/v1.0/', include("apuestas.api.urls")),
   
    # Incluir aquí las urls a views o el include a views
]