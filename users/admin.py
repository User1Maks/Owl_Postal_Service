from django.contrib import admin

from users.models import User

# Для отображения пользователей на сайте администрирования django
admin.site.register(User)

