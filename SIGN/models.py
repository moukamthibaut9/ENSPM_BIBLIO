from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


DEPARTMENTS = [
    ('INFOTEL','Informatique et Telecommunications'),
    ('HYMAE','Hydraulique et Maîtrise des Eaux'),
    ('ENREN','Energies Renouvelables'),
    ('AGEPD','Agriculture, Elevage et Produits Dérivés'),
    ('SCIENV','Sciences Environnementales '),
    ('GCA','Genie Civil et Architecture'),
    ('GTC','Génie du Textile et Cuir'),
    ('AHN','Arts et Humanités Numériques'),
    ('MC','Météorologie et Climatologie '),
]
LEVELS = [
    ('L0','Aucun'),('L1','Niveau 1'), ('L2','Niveau 2'),
    ('L3','Niveau 3'), ('L4','Niveau 4'), ('L5','Niveau 5')
]
USER_STATUS = [
    ('EL','Eleve Ingenieur'),
    ('EN','Enseignant'),
]

class MyUser(AbstractUser):
    statut = models.CharField(max_length=20, choices=USER_STATUS, default='EL', blank=False)
    department = models.CharField(max_length=100, choices=DEPARTMENTS, blank=True)
    phone_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(
            regex=r'^\+237[6][0-9]{8}$',
            message="Le numéro doit être au format +237 suivi de 9 chiffres, ex: +237612345678"
        )],
        null=True
    )
    registration_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9]{10,15}$')],
        null=True
    ) # Matricule de l'enseignant ou de l'élève
    level = models.CharField(max_length=10, choices=LEVELS, default='L0')
    pdf_doc = models.FileField(upload_to = f"Documents/Pieces_id".replace(' ','_'), blank=True, null=True)
    recto_image = models.ImageField(upload_to = f"Images/Pieces_id".replace(' ','_'), blank=True, null=True)
    verso_image = models.ImageField(upload_to = f"Images/Pieces_id".replace(' ','_'), blank=True, null=True)
    is_teacher = models.BooleanField(default=False)
    is_framer_teacher = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:  # Vérifier si l'utilisateur existe déjà en base de données
            current = MyUser.objects.get(pk=self.pk)
            # Si on active chez lui le statut d'enseignant
            if not current.is_teacher and self.is_teacher:
                subject = 'PIPO FEDERATION: Confirmation vérification statut'
                message = f"Bonjour chèr(e) {self.username}, juste pour vous informer que votre statut enseignant a été activé.\
                        \nVous pouvez à présent vous connecter et bénéficier de plus de fonctionalités\
                        \nMerci de nous faire confiance.\
                        \n\n\tCordialement, l'équipe de PIPO FEDERATION.\n"   
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=True)             
            # Si on deactive chez lui le statut d'enseignant
            elif current.is_teacher and not self.is_teacher:
                subject = 'PIPO FEDERATION: Révocation statut enseignant'
                message = f"Bonjour chèr(e) {self.username}, juste pour vous informer que votre statut enseignant a été révoqué.\
                        \nPour plus d'informations sur les raisons de cette révocation, vous pouvez nous contacter via cette adresse ou via notre formulaire de contact sur le site.\
                        \nMerci de nous faire confiance.\
                        \n\n\tCordialement, l'équipe de PIPO FEDERATION.\n" 
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=True)
        super().save(*args, **kwargs)  # Sauvegarde normale du livre