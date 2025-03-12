# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Each message belongs to a chatroom
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User authentication-ready
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.user.username} in {self.room.name}: {self.content[:20]}"
