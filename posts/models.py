from django.db import models
from accounts.models import UserProfile


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(UserProfile, related_name="postlike", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.user.username} - {self.caption}'


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    likes = models.ManyToManyField(UserProfile, related_name="postcomment", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_clikes(self):
        return self.likes.count()

    def is_liked(self):
        if self.user in self.likes.all():
            return True
        return False

    def __str__(self):
        return f'{self.post.caption} - {self.user.user.username} - {self.comment}'

