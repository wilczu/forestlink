from django.contrib import admin
from .models import User, Blocked, Page

# Register your models here.
admin.site.register(User)
admin.site.register(Blocked)
admin.site.register(Page)