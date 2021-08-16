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
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


# class UserFollowUnfollow(models.Model):
#     user_id = models.ForeignKey(
#         "User", related_name="following", on_delete=models.CASCADE)
#     following_user_id = models.ForeignKey(
#         "User", related_name="followers", on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user_id', 'following_user_id'],  name="unique_followers")
#         ]

#         ordering = ["-created"]

    # def __str__(self):
    #     f"{self.user_id} follows {self.following_user_id}"
