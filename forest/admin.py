from django.contrib import admin
from .models import User, Blocked, Page, Color, Report

# Register your models here.
admin.site.register(User)
admin.site.register(Blocked)
admin.site.register(Page)
admin.site.register(Color)
admin.site.register(Report)