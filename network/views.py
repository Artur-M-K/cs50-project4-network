import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = ['text']


def index(request):
    user = request.user
    return render(request, "network/index.html", {
        "posts": Post.objects.order_by('-timestamp'),
        "userInfo": user
    })


@login_required
def new_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreatePost
    return render(request, "network/newpost.html", {
        'form': form
    })


@login_required
def user_info(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(user=user)
    followers = user.followers.count()
    follow = user.following.count()
    return render(request, "network/user_info.html", {
        'user_id': id,
        'userInfo': user,
        'posts': posts,
        'followers': followers,
        'follow': follow
    })


# @login_required
def followers(request, id):
    user = User.objects.get(id=id)
    currentUser = User.objects.get(id=request.user.id)
    following = user.following.all()

    if id != currentUser.id:
        if currentUser in following:
            user.following.remove(currentUser.id)
        else:
            user.following.add(currentUser.id)
    return HttpResponseRedirect(reverse(user_info, args=[user.id]))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
