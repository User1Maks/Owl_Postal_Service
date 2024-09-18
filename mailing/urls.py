from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (
    index,

    ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView,
    ClientDeleteView,

    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView,
    MessageDeleteView
)

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),

    # Клиенты
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(),
         name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(),
         name='client_delete'),

    # Сообщения
    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/', MessageDetailView.as_view(),
         name='message_detail'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(),
         name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(),
         name='message_delete'),
]
