
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
    path("user_info/<int:id>/", views.user_info, name="user_info"),

    # API
    path("followers/<int:id>", views.followers, name="followers")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
