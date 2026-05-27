from .models import Post, Comment
from django import forms
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta():
        model = Post

        fields = '__all__'
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        exclude = [
            'is_published',
            'author'
        ]


class ProfileForm(forms.ModelForm):

    class Meta():
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('text',)
        widgets = {}
