from django.shortcuts import render, get_object_or_404, redirect
from .models import Objava, Profil
from .forms import PostForm
from django.http import HttpResponseForbidden

def lista_objava(request):
    objave = Objava.objects.all
    return render(request, "drustvena_mreza/lista_objava.html", {"objave": objave})

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