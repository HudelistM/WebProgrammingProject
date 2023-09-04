from django.urls import path
from .views import pocetna, lista_profila, profil,lista_objava
from django.contrib.auth import views as auth_views
from . import views as app_views
from . import views
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


User = get_user_model()

app_name = "drustvena_mrezaApp"

urlpatterns = [
    path("", pocetna, name="pocetna"),
    path("lista_profila/", lista_profila, name="lista_profila"),
    path("lista_objava/", lista_objava, name="lista_objava"),
    path("profil/<int:pk>", profil, name="profil"),
    path("register/", app_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="drustvena_mreza/login.html"), name="login"),
    path('homepage/', views.homepage, name='homepage'),
    path('moj_profil/', views.moj_profil, name='moj_profil'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('logout/', views.custom_logout, name='logout'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
    path('search/', views.search, name='search'),
]