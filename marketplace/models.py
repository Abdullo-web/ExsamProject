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
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
    
class Favorite(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE,related_name='favorites_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='favorites_post')
    cr_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','post'],
                name='unique_favorite'
                )
        ]
    def __str__(self):
        return f'{self.user.username} - {self.post.title}'
    
    
class Message(models.Model):
    sender = models.ForeignKey(UserRegister,on_delete=models.CASCADE,related_name='sent_messages')
    receiver = models.ForeignKey(UserRegister,on_delete=models.CASCADE,related_name='received_messages')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='messages')
    text = models.TextField()
    cr_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'