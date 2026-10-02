from django import forms
from .models import Profile


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','nik_profile','phone','bio']
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        if len(phone) != 13:
            raise forms.ValidationError('Номер должен содержать 13 символов.')
        
        if not phone.startswith('+992'):
            raise forms.ValidationError('Номер телефона должен начинаться с +992.')    
           
        return phone
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','nik_profile','phone','bio']
        
    
# class ProfileDetailForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['']