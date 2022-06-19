from select import select
from django.forms import ModelForm
from .models import Enrollment_form, Predmeti, Korisnik
from django import forms
from django.contrib.auth.forms import UserCreationForm  , UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
user = settings.AUTH_USER_MODEL

class CustomModelFilter(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.username, obj.email)

class SubjectForm(ModelForm):
    nositelj_predmet = CustomModelFilter(queryset=Korisnik.objects.filter(role='prof'))

    class Meta:
        model = Predmeti
        fields = ['name', 'kod', 'program','ects','sem_red','sem_izv','izborni','nositelj_predmet']

    




    
class EditProfileForm(UserChangeForm):
    template_name='edit_user.html'

    class Meta:
        model = Korisnik
        fields = (
            'username',
            'email',
            'status',
            'password'
        )

        widgets = {

        'username': forms.TextInput(attrs={'class' : 'form-control'}),
        'email': forms.EmailInput(attrs={'class' : 'form-control'}),
        'status': forms.TextInput(attrs={'class' : 'form-control'}),
        
    }
    
    


class StatusForm(ModelForm):
    class Meta:
        model = Enrollment_form
        fields = ['status']


class RegistrationForm(UserCreationForm):  

   
    username = forms.CharField(label='Username', min_length=5, max_length=150)  
    email = forms.EmailField(label='Email')  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = Korisnik.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = Korisnik.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = Korisnik.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  