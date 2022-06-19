"""Moodle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from App import views
from django.contrib.auth import views as auth_viwes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('index/', views.index, name='index'),
    path('predmeti/', views.get_subject, name='predmeti'),
    path('dodaj_predmet/', views.add_subject, name='dodaj_predmet'),
    path('studenti/', views.get_all_students, name='studenti'),
    path('profesori/', views.get_all_profesors, name='profesori'),
    path('upisni_list/<int:student_id>', views.upisni_list, name='upisni_list'),
    path('edit/<int:student_id>', views.edit_user, name='edit'),
    path('confirmdeletion/<int:subject_id>', views.deletion_confirmation, name='confirm_deletion'),
    path('deletesubject/<int:subject_id>', views.delete_subject, name='delete_subject'),
    path('studenti_po_predmetu/<int:subject_id>', views.studenti_po_predmetu, name='studenti_po_predmetu'),
    path('predmeti_po_profesoru/', views.predmeti_po_profesoru, name='predmeti_po_profesoru'),
    path('register/', views.register, name='register'),
    path('status/<int:subject_id>/<int:student_id>', views.status, name='status'),
    path('pali/<int:subject_id>', views.pali, name='pali'),
    path('imaju_potpis/<int:subject_id>', views.imaju_potpis, name='imaju_potpis'),
    path('polozili/<int:subject_id>', views.polozili, name='polozili'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password/<int:student_id>', views.change_password, name='password'),
    path('edit_predmet/<int:subject_id>', views.edit_predmet, name='edit_predmet'),
    
]
