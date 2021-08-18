from functools import wraps

from django.core.exceptions import PermissionDenied


class NicknameSlugMixin:
    """
    Установка slug полей в значение nickname для корректной работы представлений, наследующих от SingleObjectMixin
    """
    slug_field = 'nickname'
    slug_url_kwarg = 'nickname'


def check_user_permission_to_edit_profile(method):
    """
    Проверка прав пользователя на изменение состояния профиля
    """
    @wraps(method)
    def wrapper(self, request, *args, **kwargs):
        if kwargs['nickname'] != request.user.profile.nickname:
            raise PermissionDenied()
        return method(self, request, *args, **kwargs)

    return wrapper

