import random

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from drustvena_mrezaApp.models import Objava
from drustvena_mrezaApp.factory import (
    UserFactory,
    ObjavaFactory
)

NUM_USERA = 10
NUM_OBJAVA = 100

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User,Objava]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_USERA):
            user = UserFactory()

        for _ in range(NUM_OBJAVA):
            objava = ObjavaFactory()