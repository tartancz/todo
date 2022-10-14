from django.contrib import admin

from .models import ToDo, Comment
# Register your models here.

admin.site.register(ToDo)
admin.site.register(Comment)