from django.urls import path

from .views import *


urlpatterns = [
    path('all_posts/', PostListView.as_view(), name='all_posts'),
    path('search/', SearchPostsView.as_view(), name='search_posts'),
    path('post/<int:pk>/add_comment', CommentCreateView.as_view(), name='add_comment'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
]