from django.shortcuts import render, redirect
from .models import Post, Like, Comment, Reel, Story
import requests
from django.conf import settings


def posts_home(request):
    return render(request, 'posts.html')


def posts(request):

    posts = Post.objects.all().order_by('-created_at')

    

    return render(request, 'posts.html', {
        'posts': posts
    })


def create_post(request):

    if request.method == "POST":

        content = request.POST.get('content')
        image = request.FILES.get('image')


        Post.objects.create(
            user=request.user,
            content=content,
            image=image
        )


        return redirect('profile', username=request.user.username)


    return redirect('posts')


from django.shortcuts import get_object_or_404, redirect
from .models import Post


def delete_post(request,id):

    post = get_object_or_404(Post,id=id)


    if request.user == post.user:

        post.delete()


    return redirect(
        'profile',
        username=request.user.username
    )


def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)


    if request.user in post.likes.all():

        post.likes.remove(request.user)

    else:

        post.likes.add(request.user)


    return redirect('index')



def add_comment(request, post_id):

    if request.method == "POST":

        post = Post.objects.get(id=post_id)

        comment_text = request.POST.get('comment')

        Comment.objects.create(
            post=post,
            user=request.user,
            comment=comment_text
        )

    return redirect('/home/')


def index(request):

    posts = Post.objects.all().order_by('-created_at')

    story_users = {}

    all_stories = Story.objects.all().order_by('created_at')

    for story in all_stories:

        if story.user.id not in story_users:
            story_users[story.user.id] = story

    return render(
        request,
        'index.html',
        {
            'posts': posts,
            'story_users': story_users.values()
        }
    )



# ==========================
# REELS
# ==========================

def reels_page(request):

    headers = {
        "Authorization": settings.PEXELS_API_KEY
    }

    url = "https://api.pexels.com/videos/popular?per_page=20"

    response = requests.get(
        url,
        headers=headers
    )

    videos = []

    if response.status_code == 200:

        data = response.json()

        videos = data.get("videos", [])

    return render(
        request,
        "reels.html",
        {
            "videos": videos
        }
    )
    
    
    
def add_story(request):
    if request.method == "POST":
        file = request.FILES.get('story_file')
        story = Story(user=request.user )
        if file:
            if file.content_type.startswith('image'):
                story.image = file
            elif file.content_type.startswith('video'):
                story.video = file
        story.save()
        
        return redirect('/home/')
    return render(  request, 'add_story.html')




from django.shortcuts import get_object_or_404

def story_view(request, story_id):

    current_story = Story.objects.get(id=story_id)

    stories = Story.objects.filter(
        user=current_story.user
    ).order_by('created_at')

    return render(
        request,
        'story_view.html',
        {
            'stories': stories,
            'current_story': current_story
        }
    )

    
from django.shortcuts import get_object_or_404
def delete_story(request, story_id):
    story = get_object_or_404(Story,id=story_id)
    if story.user == request.user:
        story.delete()
    return redirect('/home/')

