from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def home(request):
    return render(request,'index.html')

def forum(request):
    return render(request,'forum.html')

def policy(request):
    return render(request,'policy.html')

def send_comment(request):
    user = request.user
    # Pour redirriger l'utilisateur sur la meme page(Si HTTP_REFERER est vide, redirige vers "/")
    referer = request.META.get("HTTP_REFERER", "/")
    if user.is_authenticated:
        if request.method == "POST":
            msg_object = request.POST.get('msg_object')
            msg_body = request.POST.get('msg_body')
            if msg_object and msg_body:
                full_msg_body = f"\nMessage de l'utilisateur: {user.username}\nAyant pour adresse: {user.email}.\n\n"+msg_body
                try:
                    send_mail(msg_object, full_msg_body, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER])
                    messages.success(request, "Votre message a été envoyé.")
                except:
                    messages.warning(request, "Erreur lors de l'envoi; il pourrait s'agir d'un probleme de reseau.")
    else:
        messages.info(request, "Veillez vous connecter avant de pouvoir nous envoyer votre message.")
    return redirect(referer+'#footer')
