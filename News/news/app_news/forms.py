from django import forms
from app_news.models import News, Comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class CommentsForm(forms.ModelForm):
#     class Meta:
#         model = Comments
#         fields = '__all__'


class CommentsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.is_authenticated = kwargs.pop('is_authenticated')
        super().__init__(*args, **kwargs)
        if self.is_authenticated:
            del self.fields['user_name'], self.fields['user']
        else:
            del self.fields['user']



    class Meta:
        model = Comments
        fields = ['user_name', 'user', 'comment']


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['name', 'description', 'cat']

