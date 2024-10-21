from django.forms import ModelForm

from blog.models import Blog
from mailing.forms import StyleFormMixin


class BlogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'is_published',)
