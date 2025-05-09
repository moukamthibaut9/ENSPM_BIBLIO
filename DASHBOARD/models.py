from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from SIGN.models import DEPARTMENTS




class Department(models.Model):
    name = models.CharField(max_length=100, choices=DEPARTMENTS, default='INFOTEL', blank=False, unique=True)
    image = models.ImageField(upload_to = f"Images/".replace(' ','_'))

    def __str__(self):
        return self.name.upper()


class Speciality(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-zÀ-ÿ\s]+$')], unique=True)
    image=models.ImageField(upload_to = f"Images/".replace(' ','_'))

    def __str__(self):
        return self.name.upper()


class Book(models.Model):
    submit_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality,on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-zÀ-ÿ0-9\s.-_!,\':"?]+$')])
    title = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Za-zÀ-ÿ0-9\s.-_!,\':"?]+$')])
    author = models.CharField(max_length=150, validators=[RegexValidator(r'^[A-Za-zÀ-ÿ0-9\s.-_!,\':"?]+$')])
    professional_framer = models.CharField(max_length=150, validators=[RegexValidator(r'^[A-Za-zÀ-ÿ0-9\s.-_!,\':"?]+$')])
    academic_framer = models.CharField(max_length=150, validators=[RegexValidator(r'^[A-Za-zÀ-ÿ0-9\s.-_!,\':"?]+$')])
    defense_date = models.DateTimeField()
    abstract = models.TextField(default="Aucun résumé disponible pour ce document")
    doc = models.FileField(upload_to = f"Documents/".replace(' ','_'))
    image = models.ImageField(upload_to = f"Images/".replace(' ','_'))
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.title.upper()
