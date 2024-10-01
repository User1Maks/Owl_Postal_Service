import secrets
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from users.forms import UserRegisterForm, UserProfileForm, UserModeratorForm
from users.models import User
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect


class UserCreateView(CreateView):
    """Контролер для создания пользователя"""

    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Верификация пользователя по почте"""
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Контролер для подтверждения почты"""

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контролер для редактирования профиля пользователя"""

    model = User
    form_class = UserProfileForm
    permission_required = 'users.change_profile'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('users.can_edit_is_active_users') and user.has_perm(
                'can_edit_is_active_mailing'):
            return UserModeratorForm
        raise PermissionDenied


# class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     """Контролер для удаления пользователя"""
#     model = User
#     success_url = reverse_lazy('users:profile')
#
#     def test_func(self):
#         return self.request.user.is_superuser
