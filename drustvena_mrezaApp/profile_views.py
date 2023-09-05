from django.shortcuts import render, get_object_or_404, redirect
from .models import Profil
from django.http import HttpResponseForbidden

def lista_profila(request):
    profili = Profil.objects.exclude(user=request.user)
    return render(request, "drustvena_mreza/lista_profila.html", {"profili": profili})

def profil(request, pk):
    profil = Profil.objects.get(pk=pk)
    current_user_profile = Profil.objects.get(user=request.user)
    is_following = current_user_profile.follows.filter(pk=profil.pk).exists()
    following_users = profil.follows.all()
    followed_by_users = profil.followed_by.all()

    # Debug print statements
    print(f"Debug: Following users: {following_users}")
    print(f"Debug: Followed by users: {followed_by_users}")

    return render(request, "drustvena_mreza/profil.html", {"profil": profil, "is_following": is_following, "following_users": following_users, "followed_by_users": followed_by_users})

def follow(request, pk):
    user_to_follow = get_object_or_404(Profil, pk=pk)
    current_user_profile = Profil.objects.get(user=request.user)
    print(f"Before follow: {current_user_profile.follows.all()}")
    current_user_profile.follows.add(user_to_follow)
    print(f"After follow: {current_user_profile.follows.all()}")
    return redirect('drustvena_mrezaApp:profil', pk=pk)

def unfollow(request, pk):
    user_to_unfollow = get_object_or_404(Profil, pk=pk)
    current_user_profile = Profil.objects.get(user=request.user)
    print(f"Before unfollow: {current_user_profile.follows.all()}")
    current_user_profile.follows.remove(user_to_unfollow)
    print(f"After unfollow: {current_user_profile.follows.all()}")
    return redirect('drustvena_mrezaApp:profil', pk=pk)
