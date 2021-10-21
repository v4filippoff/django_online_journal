from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ProfileForm, CustomUserCreationForm
from .utils import profile_access_check


User = get_user_model()

class SignUpView(generic.CreateView):
    """
    Отображает и обрабатывает форму создания нового пользователя
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserProfileView(generic.DetailView):
    """
    Отображает страницу пользователя
    """
    model = User
    template_name = 'accounts/profile.html'

    @method_decorator(profile_access_check)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        active_posts_id = [int(post_id) for post_id in request.POST.getlist('is_active')]
        for post in request.user.posts.all():
            post.is_active = post.id in active_posts_id
            post.save()
        return redirect(request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_permission_to_edit_profile'] = (self.kwargs['slug'] == self.request.user.slug)
        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    Отображает и обрабатывает форму редактирования профиля
    """
    model = User
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'

    def post(self, request, *args, **kwargs):
        self.old_avatar = self.get_object().avatar
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.old_avatar != form.cleaned_data['avatar']:
            self.old_avatar.delete()
        return super().form_valid(form)

    def test_func(self):
        user = self.get_object()
        return user == self.request.user