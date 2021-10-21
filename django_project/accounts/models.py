from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    slug = AutoSlugField(populate_from='username')
    registration_date = models.DateField('Registration date', auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})
    
    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/media/avatars/default_avatar.jpg"
