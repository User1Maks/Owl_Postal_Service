from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'slug', 'content', 'created_at', 'is_published',)
    list_filter = ('id', 'title', 'created_at', 'is_published',)
    search_fields = ('title', 'created_at',)

    # Предзаполняемое поле
    prepopulated_fields = {'slug': ('title',)}
