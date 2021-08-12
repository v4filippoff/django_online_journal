from django.urls import path

from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<nickname>/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<nickname>/', UserProfileView.as_view(), name='profile'),
]