from django import forms
from django.core.exceptions import ValidationError
from .models import DEPARTMENTS, LEVELS, USER_STATUS
import re



class ConnexionForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    password=forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Au plus 100 caractères sans espace','class':'form-control'}),
        required=True,
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), required=True)
    statut = forms.ChoiceField(
        choices=USER_STATUS, 
        widget=forms.Select(attrs={'class':'form-control'}),
        required=True
    )
    department = forms.ChoiceField(
        choices=DEPARTMENTS,
        widget=forms.Select(attrs={'class':'form-control'}),
        required=True
    )
    phone_number=forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={'type':'tel','placeholder': '+237612345678', 'class':'form-control'}),
        required=True
    )
    registration_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '10 à 15 caractères(Lettres et chiffres)','class':'form-control'}),
        required=True
    )
    level = forms.ChoiceField(
        choices=LEVELS,
        widget=forms.Select(attrs={'class':'form-control'}),
    )
    password=forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True)
    password_=forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]{3,100}$', username):
            raise ValidationError("Le nom d'utilisateur doit avoir 3 à 100 caractères(lettres, chiffres ou underscore uniquement)")
        return username
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+237[6][0-9]{8}$', phone_number):
            raise ValidationError("Le numéro doit être au format +237 suivi de 9 chiffres, ex: +237612345678")
        return phone_number
    def clean_registration_number(self):
        registration_number = self.cleaned_data.get('registration_number')
        if not re.match(r'^[a-zA-Z0-9]{10,15}$', registration_number):
            raise ValidationError("Le matricule doit contenir entre 10 et 15 caractères(lettres et chiffres uniquement)")
        return registration_number
