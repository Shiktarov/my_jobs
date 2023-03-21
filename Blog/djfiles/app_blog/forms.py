from django import forms
from app_blog.models import Post, Images
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body']


class UploadPostsForm(forms.Form):
    file = forms.FileField()

class MultiFileForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


