from django.contrib import admin
from .models import Category, Post, PostLike
# Register your models here.


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostLike)
