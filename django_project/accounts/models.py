from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    register_date = models.DateField('Register date', auto_now_add=True)
    avatar = models.ImageField(upload_to='user_uploads/')
    
