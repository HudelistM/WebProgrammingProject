from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Profil,Objava

User=get_user_model()
# Create your views here.

def pocetna(request):
    return render(request, "pocetna.html")
def lista_profila(request):
    profili = Profil.objects.exclude(user=request.user)
    return render(request, "drustvena_mreza/lista_profila.html", {"profili": profili})
def lista_objava(request):
    objave = Objava.objects.all
    return render(request, "drustvena_mreza/lista_objava.html", {"objave": objave})
def profil(request, pk):
    profil = Profil.objects.get(pk=pk)
    return render(request, "drustvena_mreza/profil.html", {"profil": profil})