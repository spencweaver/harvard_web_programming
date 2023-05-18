from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    like_list = models.ManyToManyField("Post", related_name="likes")
    friend_list = models.ManyToManyField("User", related_name="friends")

    def serialize(self):
        return {
            "user_id": self.id,
            "user_name": self.username
        }

    def __str__(self):
        # likes = ", ".join(str(l) for l in self.like_list.all())
        return "{} >>".format(self.username)


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.body}"

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
        }


class Message(models.Model):
    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name="messages_sent")
    Receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="messages_received")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}: {self.body}"

    def serialize(self):
        return {
        "id": self.id,
        "sender": self.sender.username,
        "body": self.body,
        "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        "read": self.read,
        "archived": self.archived
    }