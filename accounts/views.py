from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from posts.models import Follow, Post
from .models import Profile


def landing(request):
    return render(request,'landing.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username,
                email=email,password=password)
        user.save()
        return redirect('/login/')
    return render(request,'register.html')


def user_login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/home/')
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('/login/')


def profile(request, username):
    user = get_object_or_404(User,username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user,
            following=user ).exists()
    return render(request,'profile.html',{'profile_user':user,
     'posts':posts,'followers':followers,'following':following,
     'is_following':is_following })


def follow_user(request, username):
    user = get_object_or_404(User,username=username)
    if request.user != user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,following=user)
        if not created:
            follow.delete()
    return redirect('/profile/' + username + '/')



def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.bio = request.POST.get("bio")

        if request.FILES.get("profile_pic"):
            profile.profile_pic = request.FILES["profile_pic"]

        profile.save()

        return redirect(
            f"/profile/{request.user.username}/"
        )

    return render(
        request,
        "edit_profile.html",
        {"profile": profile}
    )