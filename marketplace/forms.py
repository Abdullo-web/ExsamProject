from django import forms
from .models import Post,Message


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category','oblojka','video','title','description','price','city']
        


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите сообщение...'
            })
        }