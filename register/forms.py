from django import forms
from .models import UserRegister
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = UserRegister
        fields = ['username', 'email','password1','password2']
        
        
    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if len(username) < 4:
            raise forms.ValidationError('Username должен содержать минимум 4 буквы.')
        
        if username[0] in '_.' or username[-1] in '_.':
            raise forms.ValidationError('Username не может начинаться или заканчиваться "." или "_".')
        
        for name in username:
            if not (name.islower() or name.isdigit() or name in '_.'):
                raise forms.ValidationError('Можно использовать только маленькие буквы, цифры, "." и "_".')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserRegister.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email
    