from django.contrib import admin
from .models import Comment, Content

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'text']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'text']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Content, ContentAdmin)
