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
    path('list/', BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/update', BlogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),

]
