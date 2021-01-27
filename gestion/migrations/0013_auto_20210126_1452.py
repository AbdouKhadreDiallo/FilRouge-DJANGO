# Generated by Django 3.1 on 2021-01-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0012_referentiel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referentiel',
            name='competences',
        ),
        migrations.AddField(
            model_name='referentiel',
            name='groupeCompetences',
            field=models.ManyToManyField(blank=True, to='gestion.GroupeCompetences'),
        ),
    ]