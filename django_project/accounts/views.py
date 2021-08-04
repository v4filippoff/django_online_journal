from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views import generic

from .forms import ProfileForm


class SignUpView(generic.CreateView):
    """
    Отображает и обрабатывает форму создания нового пользователя
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserProfileView(generic.TemplateView):
    template_name = 'accounts/profile.html'


class ProfileEditView(generic.FormView):
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.profile = form.cleaned_data['avatar']
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})
