# Generated by Django 4.1.4 on 2022-12-22 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drustvena_mrezaApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objava',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sadrzaj', models.CharField(max_length=200)),
                ('datum_objave', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='dweets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
