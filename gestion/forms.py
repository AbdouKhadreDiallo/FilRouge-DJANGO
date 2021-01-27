from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Profil, Admin, Teacher, GroupeCompetences, Competences, Niveaux, Referentiel
from django.db import transaction


class UserSignUpForm(UserCreationForm):
    profil = forms.ModelChoiceField(
        queryset=Profil.objects.all()
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        profil = self.cleaned_data.get('profil')
        print(profil)
        return
        if profil == '3':
            user.is_teacher = True
            user.save()
            return user
        else:
            user.is_student = True
            user.save()
            student = Student.objects.create(user=user)
            return user


class adminAddForm(UserCreationForm):
    profil = forms.ModelChoiceField(
        queryset=Profil.objects.filter(libelle='ADMIN')
    )
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    profil_pic = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.profil_pic = self.cleaned_data.get('profil_pic')
        user.profil = self.cleaned_data.get('profil')
        user.save()
        Admin.objects.create(user=user)
        return user


class teacherAddForm(UserCreationForm):
    profil = forms.ModelChoiceField(
        queryset=Profil.objects.filter(libelle='TEACHER')
    )
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    profil_pic = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.profil_pic = self.cleaned_data.get('profil_pic')
        user.profil = self.cleaned_data.get('profil')
        user.save()
        Teacher.objects.create(user=user)
        return user


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = '__all__'


class GroupeCompetenceForm(forms.ModelForm):
    competences = forms.ModelMultipleChoiceField(
        queryset=Competences.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = GroupeCompetences
        fields = '__all__'

    @transaction.atomic
    def save(self):
        groupeCompetence = super().save(commit=False)
        groupeCompetence.save()
        groupeCompetence.competences.add(*self.cleaned_data.get('competences'))
        return groupeCompetence


class CompetenceForm(forms.ModelForm):
    class Meta:
        
        model = Competences
        fields = ('libelle', 'groupeCompetences', )

class NiveauForm(forms.ModelForm):
    class Meta:
        model = Niveaux
        fields = '__all__'

class ReferentielForm(forms.ModelForm):
    class Meta:
        model = Referentiel
        fields = '__all__'
   
