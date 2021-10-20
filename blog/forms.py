from django import forms
from .models import AuthorPost, Comment

class SignUpForm(forms.ModelForm):
    class Meta:
        model = AuthorPost
        fields = [
            "title",
            "author",
            "article",
            "category",
            "status",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_on','active','post',]