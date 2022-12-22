from django.urls import path
from .views import pocetna, lista_profila, profil,lista_objava

app_name = "drustvena_mrezaApp"

urlpatterns = [
    path("", pocetna, name="pocetna"),
    path("lista_profila/", lista_profila, name="lista_profila"),
    path("lista_objava/", lista_objava, name="lista_objava"),
    path("profil/<int:pk>", profil, name="profil"),
]