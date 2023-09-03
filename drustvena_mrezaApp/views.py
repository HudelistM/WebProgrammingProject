from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Profil,Objava
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages

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
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("drustvena_mrezaApp:login")
    else:
        form = RegisterForm()
    return render(request, "drustvena_mreza/register.html", {"form": form})
def homepage(request):
    user = request.user
    profil = Profil.objects.get(user=user)
    following_users = profil.follows.all()
    posts = Objava.objects.filter(user__in=following_users).order_by('-datum_objave')
    return render(request, 'drustvena_mreza/homepage.html', {'posts': posts})

def moj_profil(request):
    user = request.user
    profil = Profil.objects.get(user=user)
    following_users = profil.follows.all()
    posts = Objava.objects.filter(user=user).order_by('-datum_objave')
    return render(request, 'drustvena_mreza/moj_profil.html', {'following_users': following_users, 'posts': posts})