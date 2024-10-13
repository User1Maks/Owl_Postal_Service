from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_cached_blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        """ Метод для подсчета количества просмотров """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    # def get_context_data(self, **kwargs):
    #     """Кеширование статей отображаемых в 'blog_detail.html' """
    #
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['blog_detail'] = get_cached_blog(self.object.slug)
    #     return context_data


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def test_func(self):
        return self.request.user.is_superuser

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_blog = form.save()
    #         new_blog.slug = slugify(new_blog.title)
    #         new_blog.save()
    #
    #     return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        return reverse('blog:blog_list', args=[self.kwargs.get('pk')])

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_blog = form.save()
    #         new_blog.slug = slugify(new_blog.title)
    #         new_blog.save()
    #
    #     return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        return self.request.user.is_superuser
