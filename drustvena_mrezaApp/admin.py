from django.contrib import admin
from .models import Profil,Objava
from django.contrib import admin
from django.contrib.auth.models import User, Group

models_list = [Profil,Objava]
admin.site.register(models_list)
#Modifikacija postojeceg django User modela
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)