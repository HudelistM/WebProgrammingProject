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
    return render(request, 'pocetna.html', {'posts': posts})

def moj_profil(request):
    if request.user.is_authenticated:
        user = request.user
        profil = Profil.objects.get(user=user)
        posts = Objava.objects.filter(user=user).order_by('-datum_objave')

        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect('drustvena_mrezaApp:moj_profil')
        else:
            form = PostForm()

        return render(request, 'drustvena_mreza/moj_profil.html', {'following_users': profil.follows.all(), 'posts': posts, 'form': form})
    else:
        return redirect('drustvena_mrezaApp:login') 

def edit_post(request, pk):
    post = get_object_or_404(Objava, pk=pk)
    if request.user != post.user:
        return HttpResponseForbidden("Nemate dozvolu za uređivanje ove objave.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('drustvena_mrezaApp:moj_profil')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'drustvena_mreza/edit_post.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(Objava, pk=pk)
    if request.user != post.user:
        return HttpResponseForbidden("Nemate dozvolu za brisanje ove objave.")
    
    if request.method == 'POST':
        post.delete()
        return redirect('drustvena_mrezaApp:moj_profil')
    
    return render(request, 'drustvena_mreza/delete_post.html')

def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('drustvena_mrezaApp:pocetna'))

def follow(request, pk):
    user_to_follow = get_object_or_404(Profil, pk=pk)
    current_user_profile = Profil.objects.get(user=request.user)
    current_user_profile.follows.add(user_to_follow)
    return redirect('drustvena_mrezaApp:profil', pk=pk)

def unfollow(request, pk):
    user_to_unfollow = get_object_or_404(Profil, pk=pk)
    current_user_profile = Profil.objects.get(user=request.user)
    current_user_profile.follows.remove(user_to_unfollow)
    return redirect('drustvena_mrezaApp:profil', pk=pk)

def search(request):
    query = request.GET.get('q')
    if query:
        results = Profil.objects.filter(Q(user__username__icontains=query))
    else:
        results = Profil.objects.none()
    return render(request, 'drustvena_mreza/search_results.html', {'results': results})