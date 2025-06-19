from functools import wraps
from django.http import HttpResponseForbidden

def groups_required(*nombres_grupos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            grupo_usuario = request.user.groups.first()  # Un solo grupo por usuario
            if grupo_usuario and grupo_usuario.name in nombres_grupos:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta vista.")
        return _wrapped_view
    return decorator
