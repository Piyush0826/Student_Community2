from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    # Add any other fields you want here, like profile picture, etc.

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
        message = models.TextField()
        response = models.TextField()
        timestamp = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Message from {self.user} at {self.timestamp}"

