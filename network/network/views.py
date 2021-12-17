from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post


def index(request):
    if request.method == "POST":
    
        # like post
        if 'liked_post' in request.POST:
            post = Post.objects.get(id = request.POST['liked_post'])
            post.liker.add(request.user)
            post.save()
                 
        # unlike post
        elif 'unliked_post' in request.POST:
            post = Post.objects.get(id = request.POST['unliked_post'])
            post.liker.remove(request.user)
            post.save()
    
    else: 
        posts = Post.objects.all().order_by("time").reverse()
    
        # pagination
        pages = Paginator(posts, 10)
        page = request.GET.get('page', 1)
        show = pages.page(page)
        return render(request, "network/index.html", {
            "posts": show
        })



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
        

@login_required
def create(request):
    if request.method == "POST":
        Post.objects.create(poster=request.user, content=request.POST['content'])
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/create.html")
        

@csrf_exempt        
def profile(request, userid):    
    if request.method == "POST":
        
        # edit post
        if request.user == User.objects.get(id = userid) and 'content' in request.POST:
            post = Post.objects.get(id = request.POST['post_id'])
            post.content = request.POST['content']
            post.save()
            
        # like post   
        elif 'liked_post' in request.POST:
            post = Post.objects.get(id = request.POST['liked_post'])
            post.liker.add(request.user)
            post.save()
                 
        # unlike post
        elif 'unliked_post' in request.POST:
            post = Post.objects.get(id = request.POST['unliked_post'])
            post.liker.remove(request.user)
            post.save()
        
        else:
        
            # follow
            if "follow" in request.POST:
                request.user.following.add(User.objects.get(id = userid))
        
            # unfollow    
            elif "unfollow" in request.POST:
                request.user.following.remove(User.objects.get(id = userid))
            return HttpResponseRedirect(reverse("profile", args=(userid,)))
    else:
        username = User.objects.get(id = userid)
        posts = Post.objects.filter(poster = username).order_by("time").reverse()
        following = username.following.all().count()
        follower = username.followers.all().count()
        status = request.user.following.filter(id = userid).count()
        
        # pagination
        pages = Paginator(posts, 10)
        page = request.GET.get('page', 1)
        show = pages.page(page)
        return render(request, "network/profile.html", {
            "username": username, "posts": show, "userid": userid, "login": request.user,
            "following": following, "follower": follower, "status": status
        })
        

@login_required
def following(request):
    if request.method == "POST":
    
        # like post
        if 'liked_post' in request.POST:
            post = Post.objects.get(id = request.POST['liked_post'])
            post.liker.add(request.user)
            post.save()
                 
        # unlike post
        elif 'unliked_post' in request.POST:
            post = Post.objects.get(id = request.POST['unliked_post'])
            post.liker.remove(request.user)
            post.save()
    
    else: 
        following = request.user.following.all()
        posts = Post.objects.filter(poster__in=following).order_by("time").reverse()
    
        # pagination
        pages = Paginator(posts, 10)
        page = request.GET.get('page', 1)
        show = pages.page(page)
        return render(request, "network/following.html", {
            "posts": show
        })


def posts(request):
    posts = Post.objects.all().order_by("time").reverse()
    return JsonResponse([post.serialize() for post in posts], safe=False)
