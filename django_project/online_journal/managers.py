from django.db import models

from .utils import active_posts


class PostManager(models.Manager):

    @active_posts
    def get_posts_ordered_by_date(self):
        """
        Возвращает активные посты, отсортированные по дате (сначала старые)
        """
        return super().get_queryset().order_by('pub_date')

    @active_posts
    def get_posts_reverse_ordered_by_date(self):
        """
        Возвращает активные посты, отсортированные по дате (сначала новые)
        """
        return super().get_queryset().order_by('-pub_date')

    def get_posts_containing(self, search_string):
        """
        Возвращает активные посты, заголовки которых содержат строку search_string
        """
        return self.get_posts_reverse_ordered_by_date().filter(title__contains=search_string)

    @active_posts
    def get_posts_ordered_by_rating(self):
        """
        Возвращает активные посты, отсортированные по количеству просмотров (сначала самые популярные)
        """
        return super().get_queryset().order_by('-rating')