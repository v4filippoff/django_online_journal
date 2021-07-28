from django.db import models
from django.urls import reverse


class PostManager(models.Manager):

    def get_active_posts(self):
        """
        Возвращает активные посты, упорядоченные по дате (сначала новые)
        """
        return super().get_queryset().filter(is_active=True).order_by('-pub_date')

    def get_posts_containing(self, search_string):
        """
        Возвращает активные посты, заголовки которых содержат строку search_string
        """
        return self.get_active_posts().filter(title__contains=search_string)


class Post(models.Model):
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Text')
    pub_date = models.DateTimeField('Published date', auto_now_add=True)
    is_active = models.BooleanField('Display a post on the site', default=True)
    rating = models.IntegerField('Views count', default=0)

    objects = PostManager()

    def __str__(self):
        """
        Возвращает строковое представление поста
        """
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    def update_rating(self):
        """
        Увеличивает счетчик просмотров поста на 1
        """
        self.rating += 1
        self.save()

    def get_comments_count(self):
        """
        Возвращает количество комментариев, относящихся к посту
        """
        return self.comments.count()

    def get_comments_ordered_by_date(self):
        """
        Возвращает комментарии поста, отсортированные по дате (сначала самые старые)
        """
        return self.comments.order_by('pub_date')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='comments')
    text = models.TextField('Text')
    pub_date = models.DateTimeField('Published date', auto_now_add=True)

    def __str__(self):
        """
        Возвращает строковое представление комментария
        """
        return self.text


