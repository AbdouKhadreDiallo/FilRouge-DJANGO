# Generated by Django 3.1 on 2021-01-20 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_user_profil'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
