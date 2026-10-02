from django.db import models
from register.models import UserRegister


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    

class Post(models.Model):
    owner = models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    oblojka = models.ImageField(upload_to='posts/',null=True,blank=True)
    video = models.FileField(upload_to='posts/videos',null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    cr_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title