from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Blocked(models.Model):
    page_url = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.page_url}"


class Page(models.Model):
    page_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=120)
    page_url = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.page_owner.username} : {self.page_name}"

class Color(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='color')
    page_color = models.CharField(max_length=60)
    text_color = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.page.page_owner} : {self.page.page_name}"