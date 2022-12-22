from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    def __str__(self):
        return self.user.username

def stvori_profil(sender, instance, created, **kwargs):
    if created:
        user_profile = Profil(user=instance)
        user_profile.save()
# Kreiranje profila za svakog novostvorenog usera.
post_save.connect(stvori_profil, sender=User)

class Objava(models.Model):
    user = models.ForeignKey(
        User, related_name="objave", on_delete=models.DO_NOTHING
    )
    sadrzaj = models.CharField(max_length=200)
    datum_objave = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return (
            f"{self.user} "
            f"({self.datum_objave:%Y-%m-%d %H:%M}): "
        )