from django.core.paginator import Paginator
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment, PostLikes
from .forms import PostForm, CommentForm


class PostListView(generic.ListView):
    """
    Отображает список постов 
    """
    model = Post
    template_name = 'online_journal/all_posts.html'
    context_object_name = 'post_list'

    ORDERED_QUERYSETS = {
        'reverse_pub_date': Post.objects.get_posts_reverse_ordered_by_date,
        'pub_date':         Post.objects.get_posts_ordered_by_date,
        'rating':           Post.objects.get_posts_ordered_by_rating,
    }

    def get_queryset(self):
        order = self.request.GET.get('order', 'reverse_pub_date')
        return self.ORDERED_QUERYSETS[order]()


class PostDetailView(generic.DetailView):
    """
    Отображает пост с комментариями
    """
    model = Post
    template_name = 'online_journal/post_detail.html'

    def get(self, request, *args, **kwargs):
        self.get_object().increment_rating()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Постраничное отображение комментариев поста
        comments = self.get_object().get_comments_ordered_by_date()
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        if self.request.user.is_authenticated:
            context['already_liked_by_user'] = self.get_object().already_liked_by_user(self.request.user)
        context['page_obj'] = page_obj
        context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Отображает и обрабатывает форму для создания поста
    """
    model = Post
    form_class = PostForm
    template_name = 'online_journal/post_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    

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


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Отображает и обрабатывает форму для создания комментария
    """
    model = Comment
    form_class = CommentForm
    template_name = 'online_journal/post_detail.html'

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        #Уменьшаем счетчики просмотров поста на единицу, чтобы при редиректе на страницу поста не увеличивать их лишний раз на 1
        self.object.post.decrement_rating()
        return self.object.post.get_absolute_url()


class TopPostsView(generic.ListView):
    """
    Отображает список популярных постов (за день, за месяц, за год)
    """
    model = Post
    template_name = 'online_journal/top_posts.html'
    context_object_name = 'post_list'

    ORDERED_QUERYSETS = {
        'day':    Post.objects.get_posts_ordered_by_daily_rating,
        'month':  Post.objects.get_posts_ordered_by_monthly_rating,
        'year':   Post.objects.get_posts_ordered_by_yearly_rating,
    }

    def get_queryset(self):
        order = self.request.GET.get('time_interval', 'day')
        return self.ORDERED_QUERYSETS[order]()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_interval'] = self.request.GET.get('time_interval', 'day')
        return context


class ChangeLikeStatusView(LoginRequiredMixin, generic.View):
    """
    Меняет состояние лайка пользователя над постом
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=kwargs['pk'])

        like, created = PostLikes.objects.get_or_create(user=user, post=post)
        if created:
            post.increment_likes_number()
        else:
            like.delete()
            post.decrement_likes_number()

        #Уменьшаем счетчики просмотров поста на единицу, чтобы при редиректе на страницу поста не увеличивать их лишний раз на 1
        post.decrement_rating()
        return redirect(post)