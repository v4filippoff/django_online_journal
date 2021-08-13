from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.urls import reverse_lazy
from django.views import generic

from .forms import ProfileForm
from .models import Profile
from .utils import NicknameSlugMixin


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


class ProfileEditView(NicknameSlugMixin, LoginRequiredMixin, generic.UpdateView):
    """
    Отображает и обрабатывает форму редактирования профиля
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'

    def get(self, request, *args, **kwargs):
        if kwargs['nickname'] != request.user.profile.nickname:
            raise Http404()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.old_avatar = self.get_object().avatar
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.old_avatar != form.cleaned_data['avatar']:
            self.old_avatar.delete()
        return super().form_valid(form)
