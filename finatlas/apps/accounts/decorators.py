from django.core.exceptions import PermissionDenied
from functools import wraps

def cargo_requerido(nome_cargo):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not request.user.role == nome_cargo:
                raise PermissionDenied # Leva para página 403 Forbidden
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator