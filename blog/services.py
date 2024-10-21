import random

from blog.models import Blog
from django.core.cache import cache
from django.conf import settings


def get_cached_blog(blog_slug):
    """Кеширование статей отображаемых в 'blog_detail.html' """

    if not settings.CACHES_ENABLED:
        return Blog.objects.filter(slug=blog_slug)

    cache_key = f'blog_list_{blog_slug}'
    blog_list = cache.get(cache_key)

    if blog_list is None:
        blog_list = Blog.objects.filter(slug=blog_slug)
        cache.set(cache_key, blog_list)

    return blog_list


def random_blog_articles(request):
    """Возвращает 3 случайные статьи и добавляет их в кеш"""

    cache_key = 'random_blog_articles'
    # Если кеш включен, пытаемся получить данные из кеша
    random_articles = cache.get(cache_key)

    if random_articles is None:
        # Получаем все статьи из базы данных
        all_articles = list(Blog.objects.all())
        # Определяем количество статей для возврата (максимум 3)
        num_articles = min(3, len(all_articles))
        # Получаем 3 случайные статьи
        random_articles = random.sample(all_articles, num_articles)
        # Сохраняем выбранные статьи в кеш на 10 минут
        cache.set(cache_key, random_articles, timeout=600)

    return random_articles
