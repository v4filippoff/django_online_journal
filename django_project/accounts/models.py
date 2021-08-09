from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    slug = models.SlugField()
    registration_date = models.DateField('Registration date', auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Profile avatar')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, slug=instance.username)
    instance.profile.save()

