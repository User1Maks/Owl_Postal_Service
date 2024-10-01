from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView
)

from mailing.forms import MessageForm, ClientForm, MailingForm
from mailing.models import Client, Message, Mailing


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['clients'] = Client.objects.all()
    #     context['messages'] = Message.objects.all()
    #     context['mailings'] = Mailing.objects.all()
    #     return context


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = 'mailing.view_client'


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.add_client'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """Метод для добавления ссылки на модель пользователя, которая
        заполняется автоматически"""
        client = form.save(commit=False)
        user = self.request.user
        client.user = user
        client.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'mailing.view_client'


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.change_client'

    def get_success_url(self):
        return reverse('mailing:client_detail',
                       args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    # permission_required = 'mailing.delete_client'
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        return self.request.user.is_superuser


class MessageListView(PermissionRequiredMixin, ListView):
    model = Message
    permission_required = 'mailing.view_message'


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                        CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.add_message'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        """Метод для добавления ссылки на модель пользователя, которая
        заполняется автоматически"""
        message = form.save(commit=False)
        user = self.request.user
        message.user = user
        message.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                        DetailView):
    model = Message
    permission_required = 'mailing.view_message'

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     self.object.view_counter += 1
    #     self.object.save()
    #     return self.object


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                        UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.change_message'

    def get_success_url(self):
        return reverse('mailing:message_detail',
                       args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                        DeleteView):
    model = Message
    permission_required = 'mailing.delete_message'
    success_url = reverse_lazy('mailing:message_list')


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = 'mailing.view_mailing'


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                        CreateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing.add_mailing'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        """Метод для добавления ссылки на модель пользователя, которая
        заполняется автоматически"""
        mailing = form.save(commit=False)
        user = self.request.user
        mailing.owner = user
        mailing.next_datetime_mailing = mailing.datetime_first_mailing
        mailing.mailing_status = 0
        mailing.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                        DetailView):
    model = Mailing
    permission_required = 'mailing.view_mailing'


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                        UpdateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing.change_mailing'

    def get_success_url(self):
        return reverse('mailing:mailing_detail',
                       args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.next_datetime_mailing = mailing.datetime_first_mailing
        mailing.save()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                        DeleteView):
    model = Mailing
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailing_list')
