from django.contrib.auth.mixins import LoginRequiredMixin
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


class ClientListView(ListView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """Метод для добавления ссылки на модель пользователя, которая
        заполняется автоматически"""
        client = form.save(commit=False)
        user = self.request.user
        client.user = user
        client.save()
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client_detail',
                       args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        """Метод для добавления ссылки на модель пользователя, которая
        заполняется автоматически"""
        message = form.save(commit=False)
        user = self.request.user
        message.user = user
        message.save()
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_detail',
                       args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        """Метод для добавления ссылки на модель пользователя, которая
        заполняется автоматически"""
        mailing = form.save(commit=False)
        user = self.request.user
        mailing.user = user
        mailing.save()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing_detail',
                       args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
