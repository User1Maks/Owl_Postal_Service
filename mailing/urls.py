from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (
    index,
    ClientListView,
    ClientCreateView,
    ClientDetailView,
    ClientUpdateView,
    ClientDeleteView
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
]
