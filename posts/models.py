from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/images/',blank=True,null=True)
    video = models.FileField(upload_to='posts/videos/',blank=True,null=True)
    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"


class Reel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Reel"


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented"


class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('post','user')

    def __str__(self):
        return f"{self.user.username} liked"


class Follow(models.Model):
    follower = models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)
    following = models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE)
    class Meta:
        unique_together = ('follower','following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    
class Story(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/images/',blank=True,null=True)
    video = models.FileField(upload_to='stories/videos/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
