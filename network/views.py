
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
        "profile": user,

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
@login_required
def like_post(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = User.objects.get(username=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(
            user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_obj.save()
            like.save()

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect('index')


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
