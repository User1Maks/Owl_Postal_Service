from django.urls import reverse
from django.utils.text import slugify
from django.db import models


from users.models import NULLABLE


class Blog(models.Model):
    """ Модель блога """
    title = models.CharField(max_length=100, verbose_name='Заголовок',
                             help_text='Введите заголовок статьи')
    slug = models.SlugField(unique=True, blank=True, verbose_name='slug',
                            max_length=100)
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(
        upload_to='blog/images',
        verbose_name='Изображение',
        **NULLABLE,
        help_text='Загрузите изображение'
    )

    views_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name='Количество просмотров',
        help_text='Количество просмотров статьи'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        editable=False,
        help_text='Дата создания статьи',

    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Опубликовать статью'
    )

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        """ Возвращает url длы статьи на основе slug """
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
