from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=60)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.creator} created {self.title}"
