from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Blacklist(models.Model):
    page_url = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.page_url}"