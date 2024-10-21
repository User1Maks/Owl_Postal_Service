from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from users.apps import UsersConfig
from django.urls import path, reverse_lazy

from users.views import (
    UserCreateView,
    ProfileUpdateView,
    UserDetailView,
    email_verification,
    UserListView,
    block_user
)

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout'),
         name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),

    path('profile/', UserDetailView.as_view(), name='user_profile'),

    path('update_profile/', ProfileUpdateView.as_view(),
         name='update_profile'),

    path('email-confirm/<str:token>/', email_verification,
         name='email-confirm'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('block_user/<int:pk>/', block_user, name='block_user'),



    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),

    path('password_reset/complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name='password_reset_complete')

]
