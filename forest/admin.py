from django.contrib import admin
from .models import User, Blacklist

# Register your models here.
admin.site.register(User)
admin.site.register(Blacklist)