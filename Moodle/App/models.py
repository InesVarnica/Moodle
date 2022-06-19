from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class Korisnik(AbstractUser):
    ROLES = (('prof', 'profesor'), ('stu', 'student'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return '%s %s %s %s ' % (self.email, self.password , self.role , self.status)


class Predmeti(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI, blank=True)
    nositelj_predmet = models.ForeignKey(Korisnik, on_delete=models.CASCADE, related_name = 'predmeti', blank=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.name, self.kod , self.program , self.ects , self.sem_red , self.sem_izv , self.izborni, self.nositelj_predmet.username)




class Enrollment_form(models.Model):
    status=models.CharField(max_length=30)
    user = models.ForeignKey(Korisnik,  on_delete=models.CASCADE, related_name = 'enrollment_form')
    subject = models.ForeignKey(Predmeti, on_delete=models.CASCADE, related_name = 'enrollment_form')

    def __str__(self):
        return '%s %s %s ' % (self.status, self.user , self.subject)

class Pomocna_tablica_neupisani_izv(models.Model):

    predmet_neupisani= models.ForeignKey(Predmeti, null=True, blank=True, on_delete=models.CASCADE, related_name = 'pomocna_tablica_izv')
    user_neupisani = models.ForeignKey(Korisnik, null=True, blank=True,  on_delete=models.CASCADE, related_name = 'pomocna_tablica_izv')

    def __str__(self):
        return '%s %s' % (self.predmet_neupisani, self.user_neupisani )

class Pomocna_tablica_neupisani_red(models.Model):

    predmet_neupisani_red= models.ForeignKey(Predmeti, null=True, blank=True, on_delete=models.CASCADE, related_name = 'pomocna_tablica_red')
    user_neupisani_red = models.ForeignKey(Korisnik, null=True, blank=True,  on_delete=models.CASCADE, related_name = 'pomocna_tablica_red')

    def __str__(self):
        return '%s %s' % (self.predmet_neupisani_red, self.user_neupisani_red )