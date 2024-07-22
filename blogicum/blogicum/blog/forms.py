from django import forms
from .models import Post, Comment


class MainForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'comment_count')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
