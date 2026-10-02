from django.db import models
from register.models import UserRegister


class Profile(models.Model):
    owner = models.OneToOneField(UserRegister,on_delete=models.CASCADE,related_name='profile_user')
    avatar = models.ImageField(upload_to='profiles',blank=True,null=True)
    nik_profile = models.CharField(max_length=75)
    phone = models.CharField(max_length=13,unique=True)
    bio = models.TextField(blank=True)
    cr_at = models.DateField(auto_now_add=True)