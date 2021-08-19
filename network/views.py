import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

from .models import User, Post, Like


class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = ['text']


def index(request):

    user = request.user
    posts = Post.objects.order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj,
        "userInfo": user,

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
def edit_user_post(request, id):
    post = Post.objects.get(pk=id)
    if request.method == 'POST':
        form = CreatePost(request.POST, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreatePost(instance=post)
    return render(request, "network/edit_post.html", {
        'form': form,
        'post': post,
        'id': id

    })


@login_required
def user_info(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(user=user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers = user.followers.count()
    follow = user.following.count()
    usersShow = user.following.all()
    return render(request, "network/user_info.html", {
        'user_id': id,
        'userInfo': user,
        'posts': page_obj,
        'followers': followers,
        'follow': follow,
        'users': usersShow
    })


@login_required
def show_followers_posts(request, id):
    user = User.objects.get(id=request.user.id)
    userShow = user.followers.all()
    posts = Post.objects.filter(user__id__in=userShow)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        'users': userShow,
        'posts': page_obj,
        'userMain': user
    })


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


@csrf_exempt
def like_post(request, id):
    # post = get_object_or_404(Post, id=request.POST.get('like'))
    # postView = Post.objects.get(id=id)
    # liked = False
    # # if request.method == "PUT":
    # #     data = json.loads(request.body)
    # if post.likes.filter(id=request.user.id).exists():
    #     # if data.get('like'):
    #     post.likes.remove(request.user)
    #     liked = False
    #     return JsonResponse(post.likes.count(), safe=False)
    # else:
    #     post.likes.add(request.user)
    #     liked = True
    # # post.save()
    #     return JsonResponse(post.likes.count(), safe=False)
    # if request.method == "GET":
    #     return JsonResponse(post.serialize(), status=201)
    #     # return JsonResponse(post.likes.count(), safe=False)
    # return HttpResponse(status=204)
    post = Post.objects.get(id=id)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data.get("like"))
        if data.get("like"):
            Like.objects.create(user=request.user, post=post)
            post.likes = Like.objects.filter(post=post).count()
            post.save()
        else:  # unlike
            Like.objects.filter(user=request.user, post=post).delete()
            post.likes = Like.objects.filter(post=post).count()
            post.save()
    return HttpResponse(status=204)


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
