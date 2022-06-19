from tokenize import group
from turtle import st, up
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from .models import Enrollment_form, Korisnik, Pomocna_tablica_neupisani_izv, Pomocna_tablica_neupisani_red, Predmeti
from .forms import StatusForm, SubjectForm, EditProfileForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth import get_user_model
from django_globals import globals
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.urls import reverse








# Create your views here.

@login_required
def index(request):
    current_user = request.user
    return render(request, 'index.html', {'current_user':current_user})
    


@login_required
def get_subject(request):
    subjects = Predmeti.objects.all()
    return render(request, 'lista_predmeta.html',{"data":subjects})

@login_required
def add_subject(request):
        if request.method == 'GET':
            subjectForm = SubjectForm()
            return render(request, 'dodavanje_predmeta.html', {'form':subjectForm})
        elif request.method == 'POST':
            subjectForm = SubjectForm(request.POST)
            if subjectForm.is_valid():
                subjectForm.save()
                cleaned_data = subjectForm.cleaned_data
                print(cleaned_data)
                return redirect('index')
        else:
            return HttpResponseNotAllowed()

@login_required
def get_all_students(request):
    studenti=Korisnik.objects.filter(role='stu')
    return render(request, 'lista_studenata.html',{"data":studenti})

@login_required
def get_all_profesors(request):
    profesori=Korisnik.objects.filter(role='prof')
    return render(request, 'lista_profesora.html',{"data":profesori})

@login_required
def upisni_list(request,student_id):
    current_user = request.user
    korisnik=Korisnik.objects.get(pk=student_id)


    
    
    
    if 'upisani' in request.POST:
        q=(request.POST)
        print(korisnik)
        print(q['upisani'])
        #upisani_p=Enrollment_form.objects.all()
        #upisani_p=Enrollment_form.objects.filter(user=korisnik)
        upisani_p=Enrollment_form.objects.filter(user=korisnik).get(subject_id=q['upisani'])
        print(upisani_p)
        upisani_p.delete()
        
        
    
    
    if 'neupisani' in request.POST:
                q=(request.POST)
                predmeti=Predmeti.objects.get(pk=q['neupisani'])
                upisni_list=Enrollment_form(status='Upisan',subject=predmeti, user=korisnik)
                upisni_list.save()



    # Redovni student #


    neupisani=Predmeti.objects.all()
    ids_n = neupisani.values_list('id', flat=True)
    upisani=Enrollment_form.objects.all().filter(user=korisnik).order_by('subject__sem_red')
    ids_u = upisani.values_list('subject_id', flat=True)
    lista_neupisanih_id_red=set(ids_n)-set(ids_u)

    neupisani_redovni=Pomocna_tablica_neupisani_red.objects.all()
    neupisani_redovni.delete()
    for i in lista_neupisanih_id_red:
        predmet=Predmeti.objects.get(pk=i)
        neupisani_redovni=Pomocna_tablica_neupisani_red(predmet_neupisani_red=predmet, user_neupisani_red=korisnik)
        neupisani_redovni.save()
    neupisani_redov=Pomocna_tablica_neupisani_red.objects.filter(user_neupisani_red=korisnik).order_by('predmet_neupisani_red__sem_red')
    


     # Izvaredni student #



    upisani_izv=Enrollment_form.objects.filter(user=student_id).order_by('subject__sem_izv')
    neupisani_izv=Predmeti.objects.all().order_by('sem_izv')
    id_neupisani_izv=neupisani_izv.values_list('id', flat=True)
    id_upisani_izv=upisani_izv.values_list('subject', flat=True)
    lista_neupisanih_id_izv=set(id_neupisani_izv)-set(id_upisani_izv)
    
    neupisani_izvanrdeni=Pomocna_tablica_neupisani_izv.objects.all()
    neupisani_izvanrdeni.delete()
    for i in lista_neupisanih_id_izv:
        predmet=Predmeti.objects.get(pk=i)
        neupisani_izvanrdeni=Pomocna_tablica_neupisani_izv(predmet_neupisani=predmet,user_neupisani=korisnik)
        neupisani_izvanrdeni.save()
    neupisani_izvan=Pomocna_tablica_neupisani_izv.objects.filter(user_neupisani=korisnik).order_by('predmet_neupisani__sem_izv')


    

   
    
    
        
    if korisnik.status == 'izv':
        print(neupisani_izvan)
        return render(request, 'upisni_list.html',{"neupisani":neupisani_izvan,'upisani':upisani_izv,'current_user':current_user,'korisnik':korisnik})
    else:
        return render(request, 'upisni_list.html',{"neupisani":neupisani_redov,'upisani':upisani,'current_user':current_user,'korisnik':korisnik})
    
        


@login_required
def delete_subject(request, subject_id):
    subject_by_id = Predmeti.objects.get(id=subject_id)
    print(request.POST)
    if 'yes' in request.POST:
        subject_by_id.delete()
        return redirect('predmeti')
    return redirect('predmeti')

@login_required
def deletion_confirmation(request, subject_id):
    if request.method == 'GET':
        return render(request, 'confirm_deletion.html', {"data":subject_id})
    return HttpResponseNotAllowed()





@login_required
def predmeti_po_profesoru(request):
    current_user = request.user
    print(current_user)
    predmeti=Enrollment_form.objects.filter(user=current_user)
    print(predmeti)
    return render(request, 'predmeti_po_profesoru.html',{"data":predmeti})

@login_required
def register(request):  
    if request.method == 'GET':
        RegisterForm = RegistrationForm()
        return render(request, 'register.html',{'form':RegisterForm })   
    else:  
        RegisterForm = RegistrationForm(request.POST)
        if RegisterForm.is_valid():
            RegisterForm.save()
            return redirect('login')  
    return HttpResponse("Something went wrong!")


@login_required
def studenti_po_predmetu(request,subject_id):
    current_user = request.user
    predmeti=Enrollment_form.objects.filter(subject=subject_id)
    pred=Predmeti.objects.get(pk=subject_id)
    if 'edit_status' in request.POST:
        return redirect('status') 
    return render(request, 'studenti_po_predmetu.html',{"data":predmeti,'c_user':current_user,'subject_id':subject_id,'pred':pred})

@login_required
def status(request,subject_id,student_id):
    current_user = request.user
    if current_user.role == 'prof':
        id = Enrollment_form.objects.filter(user=student_id).get(subject=subject_id)
        if request.method == 'GET':
            data_to_update = StatusForm(instance=id)
            return render(request, 'status.html', {'form': data_to_update})
        elif request.method == 'POST':
            print(request.POST)
            data_to_update = StatusForm(request.POST, instance=id)
            if data_to_update.is_valid():
                data_to_update.save()
                return redirect('predmeti_po_profesoru')
        else:
            return HttpResponse("Something went wrong!")
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def pali(request,subject_id):
    studenti = Enrollment_form.objects.filter(status='Izgubio potpis').filter(subject=subject_id)
    print(studenti)
    pred=Predmeti.objects.get(pk=subject_id)
    return render(request, 'pali.html', {'data': studenti})

@login_required    
def polozili(request,subject_id):
    studenti = Enrollment_form.objects.filter(status='Prosao').filter(subject=subject_id)
    print(studenti)
    pred=Predmeti.objects.get(pk=subject_id)
    return render(request, 'polozili.html', {'data': studenti,'pred':pred})

@login_required
def imaju_potpis(request,subject_id):
    studenti = Enrollment_form.objects.filter(status='Dobio potpis').filter(subject=subject_id)
    print(studenti)
    pred=Predmeti.objects.get(pk=subject_id)
    return render(request, 'imaju_potpis.html', {'data': studenti,'pred':pred})

@login_required
def edit_user(request,student_id):
    print(student_id)
    id=Korisnik.objects.get(pk=student_id)
    print(id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=id)

        if form.is_valid():
            form.save()
            return redirect(reverse('studenti'))
    else:
        form = EditProfileForm(instance=id)
        args = {'form': form ,'student_id':student_id}
        return render(request, 'edit_user.html', args)

@login_required
def change_password(request,student_id):
    id=Korisnik.objects.get(pk=student_id)
    if request.method == 'POST':
        form = SetPasswordForm(data=request.POST, user=id)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('studenti'))
        else:
            return HttpResponse("Something went wrong!")
    else:
        form = SetPasswordForm(user=id)

        args = {'form': form}
        return render(request, 'password.html', args)

@login_required
def edit_predmet(request,subject_id):
    id=Predmeti.objects.get(pk=subject_id)
    print(id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=id)

        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = SubjectForm(instance=id)
        args = {'form': form }
        return render(request, 'edit_predmet.html', args)