# Generated by Django 4.2.6 on 2024-03-06 15:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Network', '0001_initial'),
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='following', through='Network.Follow', to=settings.AUTH_USER_MODEL),
        ),
    ]
