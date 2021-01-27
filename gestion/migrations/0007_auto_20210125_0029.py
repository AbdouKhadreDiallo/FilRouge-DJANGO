# Generated by Django 3.1 on 2021-01-25 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_competences_groupecompetences'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupecompetences',
            name='competences',
            field=models.ManyToManyField(blank=True, related_name='competences', to='gestion.Competences'),
        ),
        migrations.AlterField(
            model_name='competences',
            name='groupeCompetences',
            field=models.ManyToManyField(blank=True, related_name='groupeCompetences', to='gestion.GroupeCompetences'),
        ),
    ]