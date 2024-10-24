# Generated by Django 4.2 on 2024-10-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите заголовок статьи",
                        max_length=50,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(blank=True, unique=True, verbose_name="slug"),
                ),
                ("content", models.TextField(verbose_name="Содержимое")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение",
                        null=True,
                        upload_to="blog/images",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(
                        default=0,
                        editable=False,
                        help_text="Количество просмотров статьи",
                        verbose_name="Количество просмотров",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Дата создания статьи",
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Опубликовать статью",
                        verbose_name="Опубликовано",
                    ),
                ),
            ],
            options={
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
            },
        ),
    ]
