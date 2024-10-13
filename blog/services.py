import random

from blog.models import Blog
from django.core.cache import cache
from django.conf import settings



def get_cached_blog(blog_slug):
    """Кеширование статей отображаемых в 'blog_detail.html' """

    # Если кеш включен берем данные из кеша
    if settings.CACHES_ENABLED:
        key = f'blog_list_{blog_slug}'
        blog_list = cache.get(key)
        # Если данные в кеше не найдены, получаем данные из БД и добавляем
        # их в кеш
        if blog_list is None:
            blog_list = Blog.objects.filter(slug=blog_slug)
            cache.set(key, blog_list)
    else:
        # Если кеш выключен, получаем данные из БД
        blog_list = Blog.objects.filter(slug=blog_slug)
    return blog_list


def random_blog_articles(request):
    """Возвращает 3 случайные статьи"""
    # Получаем все статьи
    all_articles = list(Blog.objects.all())
    num_articles = min(3, len(all_articles))
    # Получаем 3 случайные статьи
    random_articles = random.sample(all_articles, num_articles)

    return random_articles
