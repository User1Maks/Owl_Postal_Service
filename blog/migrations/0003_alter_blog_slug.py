# Generated by Django 4.2 on 2024-10-13 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_blog_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="slug",
            field=models.SlugField(
                blank=True, max_length=100, unique=True, verbose_name="slug"
            ),
        ),
    ]
