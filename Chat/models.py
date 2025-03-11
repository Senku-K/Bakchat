# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username

class Message(models.Model):
    room = models.CharField(max_length=50, default="Bakchodikachoda")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
