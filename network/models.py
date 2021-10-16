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
    liked = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.text

    def total_likes(self):
        return self.liked.all().count()

    # def serialize(self):
    #     return {
    #         'likes': self.likes,
    #         'isLiked': self.isLiked
    #     }


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
