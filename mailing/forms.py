import json
from django import forms
from django.forms import BooleanField
from django.utils import timezone

from mailing.models import Client, Message, Mailing


class StyleFormMixin:
    """Класс для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)
        # Делаем выбор даты удобным для пользователя и ограничиваем его
        # выбор даты рождения
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date',
                       'max': timezone.now().date().isoformat()
                       }
            )
        }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('view_counter', 'owner',)

    def clean_letter_subject(self):
        """Проверка темы письма на наличие запретных слов """
        cleaned_data = self.cleaned_data.get('letter_subject')

        with open('forbidden_words.json', 'r', encoding='utf-8') as file:
            forbidden_words = json.load(file)

        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Недопустимое слово')
        return cleaned_data

    def clean_letter_body(self):
        """Проверка текста письма на наличие запретных слов """
        cleaned_data = self.cleaned_data.get('letter_body')

        with open('forbidden_words.json', 'rt', encoding='utf-8') as file:
            forbidden_words = json.load(file)

        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Недопустимое слово")
        return cleaned_data


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = (
            'mailing_name', 'datetime_first_mailing', 'last_datetime_mailing',
            'period_mailing', 'message', 'clients',)
        widgets = {
            'datetime_first_mailing': forms.DateTimeInput(
                attrs={'type': 'datetime-local',
                       'min': timezone.now().isoformat()}),
            'last_datetime_mailing': forms.DateTimeInput(
                attrs={'type': 'datetime-local',
                       'min': timezone.now().isoformat()})
        }

    def clean_mailing_name(self):
        """Проверка названия рассылки на наличие запретных слов """
        cleaned_data = self.cleaned_data.get('mailing_name')

        with open('forbidden_words.json', 'rt', encoding='utf-8') as file:
            forbidden_words = json.load(file)

        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Недопустимое слово")
        return cleaned_data
