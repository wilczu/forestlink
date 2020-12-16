from django.contrib.auth.models import AbstractUser
from django.db import models
from fontawesome_5.fields import IconField

class User(AbstractUser):
    pass


class Blocked(models.Model):
    page_url = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.page_url}"


class Color(models.Model):
    background_color = models.CharField(max_length=60)
    text_color = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.id} : {self.text_color}"


class Page(models.Model):
    page_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=120)
    page_url = models.CharField(max_length=2000) 
    page_color = models.ForeignKey(Color, on_delete=models.CASCADE, default=0, related_name="color")
    page_icon = IconField()

    def __str__(self):
        return f"{self.page_owner.username} : {self.page_name}"