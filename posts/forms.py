from django import forms

from comments.models import Comment
from .models import Post


class PostForm(forms.ModelForm):
    username = forms.CharField(label='Имя автора')

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    username = forms.CharField(label='Имя автора')

    class Meta:
        model = Comment
        fields = ['text']