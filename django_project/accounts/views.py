from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ProfileForm
from .models import Profile
from .utils import NicknameSlugMixin, check_user_permission_to_edit_profile


class SignUpView(generic.CreateView):
    """
    Отображает и обрабатывает форму создания нового пользователя
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserProfileView(NicknameSlugMixin, generic.DetailView):
    """
    Отображает страницу пользователя
    """
    model = Profile
    template_name = 'accounts/profile.html'

    @check_user_permission_to_edit_profile
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        active_posts_id = [int(post_id) for post_id in request.POST.getlist('is_active')]
        for post in request.user.posts.all():
            post.is_active = post.id in active_posts_id
            post.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'nickname': kwargs['nickname']}))


class ProfileEditView(NicknameSlugMixin, LoginRequiredMixin, generic.UpdateView):
    """
    Отображает и обрабатывает форму редактирования профиля
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'

    @check_user_permission_to_edit_profile
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @check_user_permission_to_edit_profile
    def post(self, request, *args, **kwargs):
        self.old_avatar = self.get_object().avatar
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.old_avatar != form.cleaned_data['avatar']:
            self.old_avatar.delete()
        return super().form_valid(form)
