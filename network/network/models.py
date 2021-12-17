from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followers")
    def serialize(self):
        return {
            "id": self.id,
            "post": [post.id for post in self.posters.all()],
            "following": [following.id for following in self.following.all()],
            "follower": [follower.id for follower in self.followers.all()]
        }
    
    
class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posters")
    content = models.CharField(max_length=256)
    liker = models.ManyToManyField(User, blank=True, related_name="liked")
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.poster} posted at {self.time}"
        
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.id,
            "content": self.content,
            "liker": [liker.id for liker in self.liker.all()],
            "time": self.time
        }

