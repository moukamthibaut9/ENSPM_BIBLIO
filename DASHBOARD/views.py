from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.http import FileResponse, HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from .models import Book, Department, Speciality
from .forms import BookForm, StatutForm
from datetime import datetime
from django.conf import settings


def bad_search(chaine):
    char_in=False
    for char in chaine:
        if char in ['<','>','@','/','$','?','!','*']:
            char_in=True
            break
    return char_in

@login_required # Force l'utilisateur a se loguer pour acceder a son dashboard
def dashboard(request):
    user = request.user
    departments = Department.objects.all()
    context = {'departments':departments, 'user':user}
    return render(request, 'dashboard.html', context)

@login_required
def departments(request):
    return render(request,'departments.html', 
                {
                    'departments':Department.objects.all(),
                    'specialities':Speciality.objects.all()
                })

@login_required
def specialities(request, speciality_id):
    return render(request,'specialities.html', 
                {
                      'departments':Department.objects.all(),
                      'books':Book.objects.filter(speciality__pk=speciality_id)
                })

@login_required # Force l'utilisateur a se loguer pour acceder a la vue de recherche
def search(request):
    select = request.GET['select']
    search = request.GET['search']
    if search != "" and len(search)<=10 and not bad_search(search):
        if select == 'theme':
            return render(request, 'search.html',
                    {'books':Book.objects.filter(theme__icontains=search)})
        elif select == 'titre':
            return render(request, 'search.html',
                    {'books':Book.objects.filter(title__icontains=search)})
        elif select == 'auteur':
            return render(request, 'search.html',
                    {'books':Book.objects.filter(author__icontains=search)})
        elif select == 'date':
            return render(request, 'search.html',
                    {'books':Book.objects.filter(defense_date__icontains=search)})
        else:
            return render(request, 'search.html',
                    {'books':Book.objects.filter(speciality__name__icontains=search)})
    else:
        return redirect('dashboard')

@login_required
def pdf_download(request, speciality_id, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user
    user.save()
    # Retourner le fichier PDF
    return FileResponse(book.doc.open(), content_type='application/pdf')

@login_required
def plagiat_evaluation(request, book_1_id):
    """
        Cette fonction permet d'evaluer le taux de plagiat entre deux mémoires
    """
    if not (request.user.is_teacher and request.user.is_framer_teacher):
        raise PermissionDenied(f"Un utilisateur non autorisé ({request.user.username}) a tenté d'acceder à \
                               la page d'évaluation de plagiat via la barre d'adresse.")
    book_1 = Book.objects.get(pk=book_1_id).doc
    books = Book.objects.filter(department__pk=Book.objects.get(pk=book_1_id).department.pk)
    if request.method == 'POST':
        book_source = request.POST.get('book_source')
        if book_source == 'online':
            book_2_id = request.POST.get('book_online')
            book_2 = Book.objects.get(pk=book_2_id).doc
        else:
            book_2 = request.FILES.get('book_offline')
            if not(book_2 and book_2.content_type == 'application/pdf'):
                messages.error(request,"Seuls les fichiers PDF sont autorisés.")
                return render(request, 'plagiat_eval.html', {'books': books})
        messages.success(request,"Evaluation du plagiat terminée.")
        return render(request, 'plagiat_eval.html', {'books': books})
    return render(request, 'plagiat_eval.html', {'books': books})

@login_required
def statut_verification(request):
    """
        Cette fonction permet de vérifier le statut d'un utilisateur qui lors de son inscription \
        a indiqué qu'il est un enseignant.
    """
    if request.user.statut == 'EL' or request.user.is_teacher or request.user.is_framer_teacher:
        raise PermissionDenied(f"Un utilisateur non autorisé ({request.user.username}) a tenté d'acceder à \
                               la page de vérification de statut via la barre d'adresse.")
    if request.method=='POST':
        form=StatutForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            submit_date = datetime.now().date()
            submit_time = datetime.now().time()
            admin_emails = [email for email in settings.ADMIN_EMAILS.split(',')]
            subject = 'PIPO FEDERATION: Nouvelle Vérification de Statut'
            message = f"Bonjour, ceci est une alerte provenant de la plateforme PIPO FEDERATION\
                        \nL'utilisateur {user.username} a soumis ses informations le: {submit_date} à {submit_time}\
                        \nMerci de vous connecter à l'interface d'administration pour les vérifier et valider son statut.\n"
            # Envoyer l'email
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)
                user.last_name = form.cleaned_data['last_name']
                user.first_name = form.cleaned_data['first_name']
                user.pdf_doc = form.cleaned_data['pdf_doc']
                user.recto_image = form.cleaned_data['recto_image']
                user.verso_image = form.cleaned_data['verso_image']
                user.save()
                messages.success(request, "Vos informations ont été soumis avec success.")
            except:
                messages.error(request,"Erreur de soumission. Il se pourait que votre connexion internet soit pertubée.")
            return render(request, 'statut_verification.html', {'form':form})
        else:
            for field, errors in form.errors.items(): # pour redirriger les erreurs de formulaire vers 'messages'
                for error in errors:
                    messages.error(request, f"{field.capitalize()} : {error}")
            return render(request, 'statut_verification.html', {'form':form})
    form = StatutForm()
    return render(request, 'statut_verification.html', {'form':form})

class DocSubmit(LoginRequiredMixin,CreateView):
    model = Book
    form_class = BookForm
    template_name = 'doc_submit.html'
    success_url = '/dashboard/doc_submit'

    def form_valid(self, form):
        user = self.request.user
        form.instance.submit_by = user
        messages.success(self.request, "Le document a été soumis avec success")
        return super().form_valid(form) 
    
    

class DocUpdate(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'doc_update.html'

    def get_success_url(self):
        return reverse('specialities', kwargs={'speciality_id': self.get_object().speciality.pk})

    def dispatch(self, request, *args, **kwargs):
        if not (request.user == self.get_object().submit_by and request.user.is_teacher and request.user.is_framer_teacher):
            raise PermissionDenied(f"Un utilisateur non autorisé ({request.user}) a tenté d'acceder à la \
                                   page de modification de mémoire via la barre d'adresse")
        return super().dispatch(request, *args, **kwargs)


class DocDelete(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'doc_delete.html'

    def get_success_url(self):
        return reverse('specialities', kwargs={'speciality_id': self.get_object().speciality.pk})

    def dispatch(self, request, *args, **kwargs):
        if not (request.user == self.get_object().submit_by and request.user.is_teacher and request.user.is_framer_teacher):
            raise PermissionDenied(f"Un utilisateur non autorisé ({request.user}) a tenté d'acceder à la \
                                   page de suppression de mémoire via la barre d'adresse")
        return super().dispatch(request, *args, **kwargs)