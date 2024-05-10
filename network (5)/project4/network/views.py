from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User,Post,Follow,Like
import json  



def remove_like(request, id):
    post = Post.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    newlike = Like(user=user,post=post)
    newlike.save()
    return JsonResponse({"message": "Like added!"})


def add_like(request,id):
    post = Post.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user,post=post)
    like.delete()
    return JsonResponse({"message": "Like removed!"})



def index(request):
    allposts = Post.objects.all().order_by('-id')   
    # pagination
    paginator =  Paginator(allposts, 10)
    page_number = request.GET.get('page')
    post_of_the_page = paginator.get_page(page_number)

    allikes = Like.objects.all()

    whoYouLiked = []
    try:
        for like in allikes:
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []


    return render(request, "network/index.html", {
         "posts": allposts,
         "posts_of_the_page":post_of_the_page,
         "whoYouLiked":whoYouLiked
    })
        

def Edit(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})


def Following(request):
    current_user = request.user

    # pegando todos os ususarios que estamos seguindo
    following_users = Follow.objects.filter(user=current_user).values_list('user_follower', flat=True)

    all_posts = Post.objects.filter(user__in=following_users).order_by('-id')
    # pagination
    paginator =  Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    post_of_the_page = paginator.get_page(page_number)

    return render(request, "network/Follower.html", {
         "posts": all_posts,
         "posts_of_the_page":post_of_the_page
    })
        

def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=currentUser,user_follower=userfollowData)
    f.delete()
    id = userfollowData.id
    return HttpResponseRedirect(reverse(get_perfil,kwargs={'id': id}))

def follow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow(user=currentUser,user_follower=userfollowData)
    f.save()
    id = userfollowData.id
    return HttpResponseRedirect(reverse(get_perfil,kwargs={'id': id}))


def get_perfil(request, id):
    if request.method == "GET":
        currentUser = User.objects.get(pk=id)
        allposts = Post.objects.filter(user=currentUser).order_by('-id')   
        # pagination
        paginator =  Paginator(allposts, 10)
        page_number = request.GET.get('page')
        post_of_the_page = paginator.get_page(page_number)

        following = Follow.objects.filter(user=currentUser)
        followers = Follow.objects.filter(user_follower=currentUser)

        try:
            checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
            if len(checkFollow) != 0 :
                isFollowing = True
            else:
                isFollowing = False
        except:
            isFollowing = False

        return render(request, "network/Pefil.html", {
            "posts": allposts,
            "posts_of_the_page":post_of_the_page,
            "following":followers,
            "followers":following,
            "isFollowing":isFollowing,
            "User":currentUser
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


def newpost(request):
    if request.method == "POST":
        content = request.POST['content']
        currentUser = User.objects.get(pk=request.user.id)
        newpost = Post(content=content,user=currentUser)
        newpost.save()
        return HttpResponseRedirect(reverse(index))
