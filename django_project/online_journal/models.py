from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .managers import PostManager


User = get_user_model()

class Post(models.Model):
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Text')
    pub_date = models.DateTimeField('Published date', auto_now_add=True)
    is_active = models.BooleanField('Display a post on the site', default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='posts')
    likes_number = models.IntegerField('Likes number', default=0)

    rating = models.IntegerField('Total views count', default=0)
    daily_rating = models.IntegerField('Daily views count', default=0)
    monthly_rating = models.IntegerField('Monthly views count', default=0)
    yearly_rating = models.IntegerField('Yearly views count', default=0)

    likes = models.ManyToManyField(User, through='PostLike')

    objects = PostManager()

    class Meta:
        ordering = ['-is_active', '-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    def increment_rating(self):
        """
        Увеличивает счетчики просмотров поста на 1
        """
        self.rating += 1
        self.daily_rating += 1
        self.monthly_rating += 1
        self.yearly_rating += 1
        self.save()

    def decrement_rating(self):
        """
        Уменьшает счетчики просмотров поста на 1
        """
        self.rating -= 1
        self.daily_rating -= 1
        self.monthly_rating -= 1
        self.yearly_rating -= 1
        self.save()

    def increment_likes_number(self):
        """
        Увеличивает счетчик лайков поста на 1
        """
        self.likes_number += 1
        self.save()

    def decrement_likes_number(self):
        """
        Уменьшает счетчик лайков поста на 1
        """
        self.likes_number -= 1
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

    def already_liked_by_user(self, user):
        """
        Проверяет лайкнул ли пользователь пост
        """
        return PostLike.objects.filter(user=user, post=self).exists()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='comments')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='comments')
    text = models.TextField('Text')
    pub_date = models.DateTimeField('Published date', auto_now_add=True)

    def __str__(self):
        return self.text


class PostLike(models.Model):
    """
    Отношение многие-ко-многим. Лайки постов, проставленные пользователем
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    date = models.DateField('Like date', auto_now_add=True)


