# Generated by Django 4.0.4 on 2022-06-19 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_remove_pomocna_tablica_neupisani_izv_ects_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pomocna_tablica_neupisani_izv',
            name='user_neupisani',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pomocna_tablica', to=settings.AUTH_USER_MODEL),
        ),
    ]
