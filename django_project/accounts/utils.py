from functools import wraps

from django.core.exceptions import PermissionDenied


class NicknameSlugMixin:
    """
    Установка slug полей в значение nickname для корректной работы представлений, наследующих от SingleObjectMixin
    """
    slug_field = 'nickname'
    slug_url_kwarg = 'nickname'


def profile_access_check(view):
    """
    Проверка прав пользователя на изменение состояния профиля
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if kwargs['nickname'] != request.user.profile.nickname:
            raise PermissionDenied()
        return view(request, *args, **kwargs)

    return wrapper

