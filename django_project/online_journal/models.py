from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from .managers import PostManager


class Post(models.Model):
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Text')
    pub_date = models.DateTimeField('Published date', auto_now_add=True)
    is_active = models.BooleanField('Display a post on the site', default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='posts')
    likes = models.IntegerField('Number of likes', default=0)

    rating = models.IntegerField('Total views count', default=0)
    daily_rating = models.IntegerField('Daily views count', default=0)
    monthly_rating = models.IntegerField('Monthly views count', default=0)
    yearly_rating = models.IntegerField('Yearly views count', default=0)

    objects = PostManager()

    class Meta:
        ordering = ['-is_active', '-pub_date']

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращает строковое представление поста
        """
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    def update_rating(self):
        """
        Увеличивает счетчики просмотров поста на 1
        """
        self.rating += 1
        self.daily_rating += 1
        self.monthly_rating += 1
        self.yearly_rating += 1
        self.save()

    def get_comments_count(self):
        """
        Возвращает количество комментариев, относящихся к посту
        """
        return self.comments.count()

    def get_comments_ordered_by_date(self):
        """
        Возвращает комментарии поста, отсортированные по дате (сначала старые)
        """
        return self.comments.order_by('pub_date')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='comments')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='comments')
    text = models.TextField('Text')
    pub_date = models.DateTimeField('Published date', auto_now_add=True)

    def __str__(self):
        """
        Возвращает строковое представление комментария
        """
        return self.text


