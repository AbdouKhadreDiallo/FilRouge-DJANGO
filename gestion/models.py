from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Profil(models.Model):
    libelle = models.CharField(max_length=200)

    def __str__(self):
        return self.libelle

class ProfilSortie(models.Model):
    libelle = models.CharField(max_length=200)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profil_pic = models.ImageField(upload_to='images/',blank=True, null=True)
    profil = models.ForeignKey(Profil, blank=True, null=True, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profilSortie = models.ForeignKey(ProfilSortie, blank=True, null=True, on_delete=models.CASCADE)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
class Competences(models.Model):
    libelle = models.CharField(max_length = 250)
    groupeCompetences = models.ManyToManyField('GroupeCompetences', blank=True, related_name="competences")
    niveaux = models.ManyToManyField('Niveaux', blank=True, related_name="competences")
    class Meta:
        ordering = ['libelle']

    def __str__(self):
        return self.libelle
class GroupeCompetences(models.Model):
    libelle = models.CharField(max_length = 250)
    description = models.CharField(max_length = 250)
    class Meta:
        ordering = ['libelle']

    def __str__(self):
        return self.libelle


class Niveaux(models.Model):
    groupeAction = models.CharField(max_length=200)
    critereEvaluation = models.CharField(max_length=200)


class Referentiel(models.Model):
    libelle = models.CharField(max_length = 250)
    presentation = models.TextField(max_length=1000)
    programme = models.FileField(blank=True)
    critereEvaluation = models.TextField(max_length=1000)
    critereAdmission = models.TextField(max_length=1000)
    groupeCompetences = models.ManyToManyField(GroupeCompetences, blank=True)

    def __str__(self):
        return self.libelle
