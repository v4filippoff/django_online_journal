from functools import wraps

from django.core.exceptions import PermissionDenied


def profile_access_check(view):
    """
    Проверка прав пользователя на изменение состояния профиля
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if kwargs['slug'] != request.user.slug:
            raise PermissionDenied()
        return view(request, *args, **kwargs)

    return wrapper

