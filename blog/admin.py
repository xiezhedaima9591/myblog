from django.contrib import admin
from .models import *

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'create_time']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)