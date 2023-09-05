from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Profil,Objava
from .forms import RegisterForm,PostForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q


User=get_user_model()
# Create your views here.

def pocetna(request):
    if request.user.is_authenticated:
        current_user_profile = Profil.objects.get(user=request.user)
        following_users = current_user_profile.follows.all()
        posts = Objava.objects.filter(user__profil__in=following_users).order_by('-datum_objave')
        return render(request, "pocetna.html", {'posts': posts})
    else:
        return render(request, "pocetna.html")


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

def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('drustvena_mrezaApp:pocetna'))

def search(request):
    query = request.GET.get('q')
    if query:
        results = Profil.objects.filter(Q(user__username__icontains=query))
    else:
        results = Profil.objects.none()
    return render(request, 'drustvena_mreza/search_results.html', {'results': results})