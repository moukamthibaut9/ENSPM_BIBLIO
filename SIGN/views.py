from django.shortcuts import render, redirect
from SIGN.forms import ConnexionForm, RegistrationForm
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Pour validation du compte par mail
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import TokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model
from django.conf import settings


def sign_up(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password']==form.cleaned_data['password_']:
                # Ajout du sel au mot de passe
                user_password = form.cleaned_data['password'][:-5]+settings.SEL+form.cleaned_data['password'][-5:]
                # On recupere les infos de l'utilisateur donr certaines seront encodées dans le lien d'activation
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                statut = form.cleaned_data['statut']
                department = form.cleaned_data['department']
                phone_number = form.cleaned_data['phone_number']
                registration_number = form.cleaned_data['registration_number']
                level = form.cleaned_data['level']
                password = user_password 
                if get_user_model().objects.filter(username=username).exists():
                    messages.error(request,"Le nom que vous avez entré est déjà pris")
                    return render(request,'sign_up.html',{'registration_form':form,})
                # Création d'un utilisateur non activé
                user=get_user_model().objects.create_user(
                                            username=username, 
                                            email=email,
                                            statut=statut,
                                            department=department,
                                            phone_number=phone_number,
                                            registration_number=registration_number,
                                            level=level,
                                            password=password,
                                            is_active = False)
                user.save()
                ############ Envoi de l'email de validation #############
                subject = 'PIPO FEDERATION! Confirmez votre adresse e-mail'
                message = render_to_string('email_confirmation.html', {
                    'username': username,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': TokenGenerator().make_token(user), 
                })
                # Envoyer l'email
                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], html_message=message)
                    messages.success(request,"Un lien de confirmation de votre adresse vous a été envoyé.\
                                        \nVeillez ouvrir votre boîte et cliquez dessus avant de pouvoir vous connecter.")
                except:
                    user.delete()
                    messages.error(request,"Erreur de soumission. Il se pourait que l'adresse fournie ne soit pas valide ou \
                                    que votre connexion internet soit pertubée.")
                return render(request,'sign_up.html',{'registration_form':form,})
            else:
                messages.error(request,"Vous avez entré deux mots de passe différents.")
                return render(request,'sign_up.html',{'registration_form':form,})    
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()} : {error}")
            return render(request,'sign_up.html',{'registration_form':form,})
    form=RegistrationForm()
    return render(request,'sign_up.html',{'registration_form':form,})

def sign_in(request):
    if request.method=='POST':
        form=ConnexionForm(request.POST)
        if form.is_valid():
            user_password=form.cleaned_data['password'][:-5]+settings.SEL+form.cleaned_data['password'][-5:]
            user=authenticate(username=form.cleaned_data['username'],password=user_password)
            if user is not None and user.is_active:
                    login(request,user)
                    return redirect('dashboard')
            else:
                messages.error(request,"Informations érronées ou compte pas encore validé")
                return render(request,'sign_in.html',{'connexion_form':form,})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()} : {error}")
            return render(request,'sign_in.html',{'connexion_form':form})
    form=ConnexionForm()
    return render(request,'sign_in.html',{'connexion_form':form,})

def sign_out(request):
    for user in get_user_model().objects.filter():
        logout(request)
    return redirect('home')

# Vue qui permet de valider l'utilisateur lorsqu'il clique sur le lien de validation dans sa boite mail
def email_validation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None:
        if TokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')  # Rediriger vers la page de connexion en cas de success
        else:
            user.delete()
            messages.error(request,"Echec de la validation: lien d'activation invalide ou expiré.\n\
                    Veillez vous enregistrer à nouveau.")
            return redirect('sign_up')  # Rediriger vers la page d'enregistrement en cas d'échec
    else:
        messages.error(request,"Echec de la validation! Veillez vous enregistrer à nouveau.")
        return redirect('sign_up')  # Rediriger vers la page d'enregistrement en cas d'échec


# Relatif à la reinitialisation du mot de passe
class PasswordReset1(PasswordResetView):
    template_name = 'registration/password_reset1.html'
class PasswordReset2(PasswordResetDoneView):
    template_name = 'registration/password_reset2.html'
class PasswordReset3(PasswordResetConfirmView):
    template_name = 'registration/password_reset3.html'
class PasswordReset4(PasswordResetCompleteView):
    template_name = 'registration/password_reset4.html'
    
