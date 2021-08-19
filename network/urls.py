
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="newpost"),
    path("edit_post/<int:id>/", views.edit_user_post, name="edit_post"),
    path("user_info/<int:id>/", views.user_info, name="user_info"),
    path("following/<int:id>/", views.show_followers_posts, name="following"),

    # API
    path("followers/<int:id>", views.followers, name="followers"),
    path("like/<int:id>", views.like_post, name="like")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
