from django.urls import path
from . import views

urlpatterns = [

    path('', views.posts, name='feed'),
    path('posts/', views.posts, name='posts'),
    path('create/', views.create_post, name='create_post'),
    path('delete-post/<int:id>/',views.delete_post,name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('home/', views.index, name='index'),
    path('reels/', views.reels_page, name='reels'),
    path('add-story/',views.add_story,name='add_story'),
    path('story/<int:story_id>/',views.story_view,name='story_view'),
    path('delete-story/<int:story_id>/',views.delete_story,name='delete_story'),

    

]