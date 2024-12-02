from django.contrib import admin
from posts.models import Post, Group, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Comment)
