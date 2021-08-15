from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='images',  default='images/user.png')


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
