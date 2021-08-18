from functools import wraps


def active_posts(get_queryset):
    """
    Декоратор, который фильтрует набор постов QuerySet по статусу активности
    """
    @wraps(get_queryset)
    def wrapper(self, *args, **kwargs):
        queryset = get_queryset(self, *args, **kwargs)
        return queryset.filter(is_active=True)
    return wrapper
