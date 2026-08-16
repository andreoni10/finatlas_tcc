from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            # Como o modelo padrão do Django permite e-mails duplicados,
            # usamos .filter().first() para evitar erros caso existam e-mails iguais.
            user = UserModel.objects.filter(email__iexact=username).first()
            
            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None
        return None