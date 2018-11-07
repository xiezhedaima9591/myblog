# -*- coding:utf-8 -*-
from django.db import models
from blog.models import Post

# Create your models here.


class Comment(models.Model):
    """
    评论表
    """
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    email = models.EmailField(max_length=255, verbose_name=u'邮箱地址')
    text = models.TextField(verbose_name=u'评论正文')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'提交时间')
    post = models.ForeignKey(Post, verbose_name=u'关联文章', on_delete=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']
        verbose_name = u'文章评论'
        verbose_name_plural = verbose_name


class Content(models.Model):
    """
    留言表
    """
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    email = models.EmailField(max_length=255, verbose_name=u'邮箱地址')
    text = models.TextField(verbose_name=u'评论正文')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'提交时间')

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']
        verbose_name = u'留言'
        verbose_name_plural = verbose_name
