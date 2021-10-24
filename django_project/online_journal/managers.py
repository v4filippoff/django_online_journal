from django.db import models


class PostManager(models.Manager):

    def get_active_posts(self):
        """
        Возвращает активные посты
        """
        return super().get_queryset().filter(is_active=True)

    def get_posts_ordered_by_date(self):
        """
        Возвращает посты, отсортированные по дате (сначала старые)
        """
        return self.get_active_posts().order_by('pub_date')

    def get_posts_reverse_ordered_by_date(self):
        """
        Возвращает посты, отсортированные по дате (сначала новые)
        """
        return self.get_active_posts()

    def get_posts_containing(self, search_string):
        """
        Возвращает посты, заголовки которых содержат строку search_string
        """
        return self.get_active_posts().filter(title__contains=search_string)

    def get_posts_ordered_by_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров (сначала самые популярные)
        """
        return self.get_active_posts().order_by('-rating')

    def get_posts_ordered_by_daily_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров за день (сначала самые популярные)
        """
        return self.get_active_posts().order_by('-daily_rating')

    def get_posts_ordered_by_monthly_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров за месяц (сначала самые популярные)
        """
        return self.get_active_posts().order_by('-monthly_rating')

    def get_posts_ordered_by_yearly_rating(self):
        """
        Возвращает посты, отсортированные по количеству просмотров за год (сначала самые популярные)
        """
        return self.get_active_posts().order_by('-yearly_rating')