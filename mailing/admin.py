from django.contrib import admin

from mailing.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'last_name', 'first_name', 'patronymic', 'date_of_birth')
    list_filter = ('id', 'email', 'last_name', 'date_of_birth',)
    search_fields = ('id', 'email', 'last_name', 'first_name', 'patronymic',)
