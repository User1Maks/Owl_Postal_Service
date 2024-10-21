from smtplib import SMTPException

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
import secrets
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView
)
from users.forms import UserRegisterForm, UserProfileForm, UserModeratorForm
from users.models import User
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контролер для отображения списка пользователей"""

    model = User
    permission_required = 'users.view_user'


class UserCreateView(CreateView):
    """Контролер для создания пользователя"""

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Верификация пользователя по почте"""
        user = form.save()
        user.is_active = False  # Делаем пользователя неактивным, пока он не
        # подтвердит почту
        token = secrets.token_hex(16)  # Создаем токен для подтверждения
        user.token = token  # Сохраняем токен в модели пользователя
        user.save()  # Сохраняем пользователя в базу данных

        # Проверяем, существует ли группа "users"
        try:

            # Получаем группу "users" из базы данных
            users_group = Group.objects.get(name='users')

            # Если пользователя нет в группе "users, то добавляем его
            if not users_group.user_set.filter(id=user.id).exists():
                users_group.user_set.add(user)
        except Group.DoesNotExist as e:
            print(f'{e} - загрузите фикстуру "groups.json" ')

        # Создаем ссылку для подтверждения почты
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'

        try:

            # Отправляем письмо с подтверждением почты
            send_mail(
                subject='Подтверждение почты',
                message=f'Перейдите по ссылке для подтверждения почты: {url}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        except SMTPException as e:
            print(f'Ошибка при отправке письма: {e}')
        return super().form_valid(form)


def email_verification(request, token):
    """Контролер для подтверждения почты"""

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Контролер для просмотра информации о пользователе"""
    model = User
    permission_required = 'users.view_user'
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контролер для редактирования профиля пользователя"""

    model = User
    form_class = UserProfileForm
    permission_required = 'users.change_user'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('users.can_edit_is_active_users') and user.has_perm(
                'mailing.can_disable_mailing_status'):
            return UserModeratorForm
        return UserProfileForm


@login_required
@permission_required('can_edit_is_active_users')
def block_user(request, pk):
    """Контролер для блокировки пользователя"""
    user = User.objects.get(pk=pk)
    user.is_active = False
    user.save()


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контролер для удаления пользователя"""
    model = User
    success_url = reverse_lazy('users:profile')

    def test_func(self):
        return self.request.user.is_superuser
