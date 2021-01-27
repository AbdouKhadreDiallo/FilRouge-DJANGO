from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth import get_user_model, logout
from .forms import UserSignUpForm, adminAddForm, teacherAddForm, ProfilForm, GroupeCompetenceForm, CompetenceForm, NiveauForm, ReferentielForm
User = get_user_model()
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import student_required, admin_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Profil, GroupeCompetences, Competences, Referentiel
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory

# Create your views here.
decorator = [login_required(), admin_required()]
@login_required()
@admin_required()
def index(request):
    return render(request, 'base.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get email value from form
        password = request.POST.get('password')  # Get password value from form

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if user.is_authenticated and user.is_student == True:
                return redirect('/student')
            elif user.is_authenticated and user.is_admin == True:
                return redirect('/accueil')
            else:
                return redirect('/login')
    return render(request, 'registration/login.html')
@login_required()
@admin_required()
def adminPage(request):
    context = {}
    user_list = User.objects.all()
    query = request.GET.get('q')
    NumberOfAllUsers = User.objects.all().count()
    admins = User.objects.filter(is_admin = True).count()
    students = User.objects.filter(is_student = True).count()
    teachers = User.objects.filter(is_teacher = True).count()

    if query:
        user_list = User.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(user_list, 6) # 6 posts per page
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    print(admins)
    context['admins'] = admins
    context['students'] = students
    context['teachers'] = teachers
    context['users'] = users
    return render(request, 'accueil/users/admin.html', context)


def student(request):
    return render(request, 'accueil/users/students.html')

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'
@method_decorator(decorator, name='dispatch')
class StudentSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'

    

    def form_valid(self, form):
        print(form)
        user = form.save()
        print(user)
        login(self.request, user)
@method_decorator(decorator, name='dispatch')
class AdminAddView(CreateView):
    model = User
    form_class = adminAddForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['action'] = "ADD"
        kwargs['user_type'] = 'ADMIN'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        print(form)
        form.save()
        return redirect('/accueil')
@method_decorator(decorator, name='dispatch')
class TeacherAddView(CreateView):
    model = User
    form_class = teacherAddForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['action'] = "ADD"
        kwargs['user_type'] = 'TEACHER'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        print(form)
        form.save()
        return redirect('/accueil')

class AdminUpdate(UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'profil_pic', )
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['action'] = "UPDATE"
        kwargs['user_type'] = 'USER'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        # print(form)
        form.save()
        return redirect('/accueil')
class UsersdeleteUser(DeleteView):
    model = User
    success_url = '/accueil'

#Gsetion profil
@method_decorator(decorator, name='dispatch')
class ProfilListView(CreateView):
    form_class = ProfilForm
    template_name = 'accueil/users/profil/profil_list.html'
    def form_valid(self, form):
        #print(form)
        form.save()
        return redirect('/accueil/profils')

    def get_context_data(self, **kwargs):
        kwargs['profil_list'] = Profil.objects.order_by('id')
        kwargs['top'] = "add Profil"
        kwargs['btn'] = "Ajouter"
        return super(ProfilListView, self).get_context_data(**kwargs)
@method_decorator(decorator, name='dispatch')
class ProfilUpdate(UpdateView):
    model = Profil
    fields = ('libelle', )
    template_name = 'accueil/users/profil/profil_list.html'

    def form_valid(self, form):
        #print(form)
        form.save()
        return redirect('/accueil/profils')

    def get_context_data(self, **kwargs):
        kwargs['profil_list'] = Profil.objects.order_by('id')
        kwargs['top'] = "update Profil"
        kwargs['btn'] = "Modifier"
        return super().get_context_data(**kwargs)
@method_decorator(decorator, name='dispatch')
class Profildelete(DeleteView):
    model = Profil
    template_name = 'gestion/user_confirm_delete.html'
    success_url = '/accueil/profils'


@method_decorator(login_required(), name='dispatch')
class ProfilDetail(DetailView):
    model = Profil
    template_name = 'accueil/users/profil/profil_detail.html'
    def get_context_data(self, **kwargs):
        kwargs['users_number'] = User.objects.filter(profil_id=self.kwargs.get('pk')).count()
        kwargs['users'] = User.objects.filter(profil_id = self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)


@method_decorator(decorator, name='dispatch')
class GroupCompetencesView(CreateView):
    form_class = GroupeCompetenceForm
    template_name = 'accueil/Parametres/GroupeCompetences/add-groupeCompetences.html'
    def form_valid(self, form):
        groupeCompetence = form.save()
        return redirect('/accueil')

@login_required()
@admin_required()
def listGroupeComptence(request):
    context = {}
    groupeComptence = GroupeCompetences.objects.all()
    # competence = groupeComptence.competences.all()
    context['groupeComptence'] = groupeComptence
    # context['competence'] = competence
    return render(request, 'accueil/Parametres/GroupeCompetences/list-groupeCompetences.html', context)

@method_decorator(login_required(), name='dispatch')
class UpdateGroupeComptence(UpdateView):
    model = GroupeCompetences
    fields = ('libelle','description',)
    template_name = 'accueil/Parametres/GroupeCompetences/add-groupeCompetences.html'

    def form_valid(self, form):
        #print(form)
        form.save()
        return redirect('/accueil/groupeCompetences/list')

@login_required()
@admin_required()
def listComptence(request):
    context = {}
    competences = GroupeCompetences.objects.all()
    for compet in competences:
        grp = compet.competences.all()
        for gr in grp:
            print(gr.libelle)
        
    print(competences)
    # competence = groupeComptence.competences.all()
    context['competences'] = competences
    

    # context['competence'] = competence
    return render(request, 'accueil/Parametres/Competences/list-competence.html', context)

@login_required()
@admin_required()
def AddCompetence(request):
    print('hop')
    niveauFormSet = formset_factory(NiveauForm, min_num=2, validate_min=True)
    if request.method == 'POST':
        print('yes')
        form = CompetenceForm(request.POST)
        niveaux = niveauFormSet(request.POST)
        if all([form.is_valid(), niveaux.is_valid()]):
            competence = form.save()
            for niveau in niveaux:
                if niveau.cleaned_data:
                    choice = niveau.save(commit=False)
                    choice.save()
                    competence.niveaux.add(choice)
                    
            return redirect('/accueil')
        print("something went wrong")
    else:
        form = CompetenceForm
        niveaux = niveauFormSet
    template_name = 'accueil/Parametres/Competences/add-competences.html'
    
    return render(request, template_name, {'form': form, 'formset': niveaux})


@method_decorator(decorator, name='dispatch')
class updateCompetence(UpdateView):
    model = Competences
    fields = ('libelle', 'groupeCompetences', 'niveaux', )
    template_name = 'accueil/Parametres/Competences/add-competences.html'

    def form_valid(self, form):
        #print(form)
        form.save()
        return redirect('/accueil')

@method_decorator(decorator, name='dispatch')
class GroupeComptenceDetail(DetailView):
    model = GroupeCompetences
    template_name = 'accueil/Parametres/Competences/list-competence.html'
    def get_context_data(self, **kwargs):
        kwargs['competences'] =  GroupeCompetences.objects.all()
        # kwargs['users'] = User.objects.filter(profil_id = self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)

@login_required()
@admin_required()
def detailGrpCompetence(request, pk, template_name='accueil/Parametres/Competences/list-competence.html'):
    context = {}
    groupeCompetence = get_object_or_404(GroupeCompetences, pk=pk)
    context['competences'] =  GroupeCompetences.objects.all()
    context['groupeCompetence'] = groupeCompetence
    return render(request, template_name, context)

@login_required()
@admin_required()
def detailCompetence(request, pk, template_name='accueil/Parametres/Competences/list-competence.html'):
    context = {}
    competence = get_object_or_404(Competences, pk=pk)
    context['competences'] =  GroupeCompetences.objects.all()
    context['competence'] = competence
    return render(request, template_name, context)


    

@method_decorator(decorator, name='dispatch')
class ReferentielCreate(CreateView):
    form_class = ReferentielForm
    template_name = 'accueil/Parametres/referentiel/add-ref.html'
    def form_valid(self, form):
        referentiel = form.save()
        return redirect('/accueil/referentiel/list')

@login_required()
@admin_required()
def listref(request):
    context = {}
    ref = Referentiel.objects.all()
    # competence = groupeComptence.competences.all()
    context['ref'] = ref
    # context['competence'] = competence
    return render(request, 'accueil/Parametres/referentiel/list-ref.html', context)


@method_decorator(decorator, name='dispatch')
class updateRef(UpdateView):
    model = Referentiel
    fields = ('libelle', 'presentation', 'programme','critereEvaluation', 'critereAdmission','groupeCompetences', )
    template_name = 'accueil/Parametres/referentiel/add-ref.html'

    def form_valid(self, form):
        #print(form)
        form.save()
        return redirect('/accueil/referentiel/list')

@method_decorator(decorator, name='dispatch')
class DetailRef(DetailView):
    model = Referentiel
    template_name = 'accueil/Parametres/referentiel/detail-ref.html'
