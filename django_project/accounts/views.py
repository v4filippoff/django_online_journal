from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import generic

from .forms import ProfileForm
from .models import Profile


class SignUpView(generic.CreateView):
    """
    Отображает и обрабатывает форму создания нового пользователя
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserProfileView(generic.DetailView):
    model = Profile
    template_name = 'accounts/profile.html'


class ProfileEditView(LoginRequiredMixin, generic.FormView):
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'

    def get(self, request, *args, **kwargs):
        if kwargs['slug'] != request.user.profile.slug:
            raise Http404()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.profile = form.cleaned_data['avatar']
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.kwargs['slug']})
