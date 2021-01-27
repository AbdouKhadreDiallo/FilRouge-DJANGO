from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.loginUser, name="login"),
    path('login/', views.loginUser, name="login"),
    path('accueil/', include(([
        path('', views.adminPage, name="admin"),
        path('user/<int:pk>/delete/', views.UsersdeleteUser.as_view(), name="delete"),
        path('profils/', views.ProfilListView.as_view(), name="list_profil"),
        path('profils/<int:pk>', views.ProfilUpdate.as_view(), name="update_profil"),
        path('profils/<int:pk>/delete/', views.Profildelete.as_view(), name="delete_profil"),
        path('profils/<int:pk>/detail/', views.ProfilDetail.as_view(), name="detail_profil"),
        path('groupeCompetences/add', views.GroupCompetencesView.as_view(), name="add_grpCompetences"),
        path('groupeCompetences/list', views.listGroupeComptence, name="list_grpCompetences"),
        path('groupeCompetences/<int:pk>/edit', views.UpdateGroupeComptence.as_view(), name="edit_grpCompetences"),
        path('groupeCompetences/<int:pk>/detail/', views.detailGrpCompetence, name="detail_competence"),
        path('competences/add', views.AddCompetence, name="add_competence"),
        path('competences/list', views.listComptence, name="list_competence"),
        path('competences/<int:pk>/edit', views.updateCompetence.as_view(), name="edit_competence"),
        path('competences/<int:pk>/detail/', views.detailCompetence, name="detailCompetence"),
        path('referentiel/add', views.ReferentielCreate.as_view(), name="add_ref"),
        path('referentiel/list', views.listref, name="list_ref"),
        path('referentiel/<int:pk>/update/', views.updateRef.as_view(), name="update_ref"),
        path('referentiel/<int:pk>/details/', views.DetailRef.as_view(), name="detail_ref"),



    ], 'admin'), namespace="admin" )),
    #path('accueil/', views.admin, name="admin"),
    path('student/', views.student, name="student"),

]   