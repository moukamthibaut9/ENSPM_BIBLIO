from django.urls import path, include
from . import views

urlpatterns = [
    path('sign_up/',views.sign_up,name='sign_up' ),
    path('sign_in/',views.sign_in,name='sign_in' ),
    path('sign_out/',views.sign_out,name='sign_out' ),
    # Vues de reinitialisation du mot de passe
    path('password_reset/', views.PasswordReset1.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordReset2.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordReset3.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordReset4.as_view(), name='password_reset_complete'),
    # Vues pour confirmation et validation de l'adresse e-mail
    path('email_validation/<uidb64>/<token>/', views.email_validation, name='email_validation'),
]