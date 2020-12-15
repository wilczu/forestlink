from django.contrib import admin
from .models import User, Blocked, Page, Color

# Register your models here.
admin.site.register(User)
admin.site.register(Blocked)
admin.site.register(Page)
admin.site.register(Color)