from django.views import generic
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostListView(generic.ListView):
    """
    Отображает список постов 
    """
    model = Post
    template_name = 'online_journal/all_posts.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        ordered_querysets = {
            'reverse_pub_date': Post.objects.get_posts_reverse_ordered_by_date,
            'pub_date':         Post.objects.get_posts_ordered_by_date,
            'rating':           Post.objects.get_posts_ordered_by_rating,
        }
        order = self.request.GET.get('order', 'reverse_pub_date')

        return ordered_querysets[order]()


class PostDetailView(generic.DetailView):
    """
    Отображает пост с комментариями
    """
    model = Post
    template_name = 'online_journal/post_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            self.get_object().update_rating()
        except AttributeError:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostCreateView(generic.CreateView):
    """
    Отображает и обрабатывает форму для создания поста
    """
    model = Post
    form_class = PostForm
    template_name = 'online_journal/post_create.html'
    

class SearchPostsView(generic.ListView):
    """
    Отображает список активных постов, удовлетворяющих поисковому запросу
    """
    model = Post
    template_name = 'online_journal/search_posts.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        search_string = self.request.GET.get('q', '')
        return Post.objects.get_posts_containing(search_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_string'] = self.request.GET.get('q', '')
        return context


class CommentCreateView(generic.CreateView):
    """
    Отображает и обрабатывает форму для создания комментария
    """
    model = Comment
    form_class = CommentForm
    template_name = 'online_journal/post_detail.html'

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})