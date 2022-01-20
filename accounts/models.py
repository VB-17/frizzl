from django.db import models
from django.contrib.auth.models import User as BaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.jpg", upload_to='profile_pics/', blank=True)
    bio = models.TextField(default="", max_length=300, blank=True)
    followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def profile_posts(self):
        return self.post_set.all()

    def profile_url(self):
        return f'/user/{self.user.username}'

    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created: 
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=BaseUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()