from django.contrib import admin
from .models import User, Page, Color, Report

# Register your models here.
admin.site.site_header = 'ForestLink'
admin.site.site_title = 'ForestLink - Admin panel'

admin.site.register(User)
admin.site.register(Page)
admin.site.register(Color)
admin.site.register(Report)