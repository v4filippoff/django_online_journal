from django.urls import path

from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<username>', UserProfileView.as_view(), name='profile'),
]