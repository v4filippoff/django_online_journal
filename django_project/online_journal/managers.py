from django.db import models

from .utils import active_posts


class PostManager(models.Manager):

    @active_posts
    def get_posts_ordered_by_date(self):
        """
        Возвращает посты, отсортированные по дате (сначала старые)
        """
        return super().get_queryset().order_by('pub_date')

    @active_posts
    def get_posts_reverse_ordered_by_date(self):
        """
        Возвращает посты, отсортированные по дате (сначала новые)
        """
        return super().get_queryset()

    @active_posts
    def get_posts_containing(self, search_string):
        """
        Возвращает посты, заголовки которых содержат строку search_string
        """
        return self.get_queryset().filter(title__contains=search_string)

    @active_posts
    def get_posts_ordered_by_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров (сначала самые популярные)
        """
        return super().get_queryset().order_by('-rating')

    @active_posts
    def get_posts_ordered_by_daily_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров за день (сначала самые популярные)
        """
        return super().get_queryset().order_by('-daily_rating')

    @active_posts
    def get_posts_ordered_by_monthly_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров за месяц (сначала самые популярные)
        """
        return super().get_queryset().order_by('-daily_rating')

    @active_posts
    def get_posts_ordered_by_yearly_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров за год (сначала самые популярные)
        """
        return super().get_queryset().order_by('-yearly_rating')