from django import forms
from django.core.exceptions import ValidationError
from .models import Book
from django.contrib.auth import get_user_model

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['department','speciality','theme','title','author',
                  'professional_framer','academic_framer','defense_date',
                  'abstract','doc','image']
        labels = {
            'department':'Quel est le département concerné par ce mémoire?',
            'speciality':'Quelle spécialité de ce département?',
            'theme':'Quelle est la thématique générale associée au mémoire?',
            'title':'Spécifiez lui un titre',
            'author':'Entrez le nom de l\'auteur du mémoire',
            'professional_framer':'Entrez le nom de l\'encadreur professionnel',
            'academic_framer':'Entrez le nom de l\'encadreur académique',
            'defense_date':'Quand est ce que le mémoire a été soutenu?',
            'abstract':'Indiquez ici le résumé et/ou l\'abstract du mémoire',
            'doc':'Selectionnez le document en question',
            'image':'Choisissez l\'image de la premiere de couverture de votre document'
        }
        widgets = {
            'department':forms.Select(attrs={'class':'form-control'}),
            'speciality':forms.Select(attrs={'class':'form-control'}),
            'theme':forms.TextInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control'}),
            'professional_framer':forms.TextInput(attrs={'class':'form-control'}),
            'academic_framer':forms.TextInput(attrs={'class':'form-control'}),
            'defense_date':forms.DateInput(attrs={ 'class': 'form-control','type':'date' }),
            'abstract':forms.Textarea(attrs={'class':'form-control','rows':10}),
            'doc':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def clean_doc(self):
        file = self.cleaned_data.get('doc')
        if file and hasattr(file, 'content_type'):
            if file.content_type != 'application/pdf':
                raise ValidationError('Uniquement les fichiers PDF sont acceptés.')
            if file.size > 5 * 1024 * 1024:
                raise ValidationError('Le fichier est trop volumineux. Taille maximale : 5Mo.')
        return file
        

class StatutForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['last_name','first_name','pdf_doc','recto_image','verso_image']
        labels = {
            'last_name':'Entrez votre nom complet',
            'first_name':'Entrez votre prénom complet',
            'pdf_doc':'Téléversez un document pdf de votre pièce d\'identité',
            'recto_image':'Téléversez une photo claire du recto de votre pièce d\'identité',
            'verso_image':'Téléversez une photo claire du verso de votre pièce d\'identité',
        }
        widgets = {
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'pdf_doc': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'recto_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'verso_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def clean_pdf_doc(self):
        file = self.cleaned_data.get('pdf_doc')
        if file and hasattr(file, 'content_type'):
            if file.content_type != 'application/pdf':
                raise ValidationError('Uniquement les fichiers PDF sont acceptés.')
            if file.size > 2 * 1024 * 1024:
                raise ValidationError('Le fichier est trop volumineux. Taille maximale : 2Mo.')
        return file