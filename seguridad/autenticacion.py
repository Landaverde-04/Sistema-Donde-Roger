from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class UsuarioBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            # Aquí es donde validas si está habilitado
            if not user.estaHabilitadoUsuario:
                return None
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
