from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from django.urls import path

from blog.views import (
    BlogListView,
    BlogCreateView,
    BlogUpdateView,
    BlogDetailView,
    BlogDeleteView
)


app_name = BlogConfig.name

urlpatterns = [
    path('list/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create', BlogCreateView.as_view(), name='blog_create'),
    path('<slug:slug>/update', BlogUpdateView.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog_delete'),

]
