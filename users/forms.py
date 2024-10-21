from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма для изменения профиля пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'avatar', 'phone', 'a_country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()  # Для скрытия
        # поля пароля в форме профиля


class UserModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'avatar', 'phone', 'a_country','is_staff')
