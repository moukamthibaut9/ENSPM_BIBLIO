from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generation d'un token unique pour un utilisateur quelconque qui s'inscrit sur le site
    """
    def _make_hash_value(self, user, timestamp):
        # Le token contiendra l'identifiant unique de l'utilisateur,
        # le moment où le token est généré (encodé dans le token lui-même),
        # l'état d’activation du compte.  
        return f"{user.pk}{timestamp}{user.is_active}"