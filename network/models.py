from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='images',  default='images/user.png')
    following = models.ManyToManyField(
        "self", blank=True, related_name="followers", symmetrical=False
    )

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    isLiked = models.BooleanField()

    def __str__(self):
        return self.text

    # def total_likes(self):
    #     return self.likes.count()

    def serialize(self):
        return {
            'likes': self.likes,
            'isLiked': self.isLiked
        }


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likeduser")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likedpost")
