# -*- coding:utf-8 -*-
import markdown
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    """
    类别模型
    """
    name = models.CharField(max_length=50, verbose_name=u'类别名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'博文类型'
        verbose_name_plural = u'博文类型'
        ordering = ['name']


class Tag(models.Model):
    """
    标签模型
    """
    name = models.CharField(max_length=50, verbose_name=u'标签名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


class User(User):
    """
    重写User,增加职业和简介字段
    """
    we_chat = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'微信号')
    QR_code = models.ImageField(upload_to='media/user_photo/%Y/%m', default='images/default.jpg',
                                max_length=100, verbose_name=u'微信二维码')
    photo = models.ImageField(upload_to='media/user_photo/%Y/%m', default='images/default.jpg',
                              max_length=100, verbose_name=u'用户头像')
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'职业')
    introduction = models.CharField(max_length=255, verbose_name=u'用户简介')
    talk_to_myself = models.TextField(verbose_name=u'自白', blank=True, null=True)

    def __str__(self):
        return super(User, self).get_full_name()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'
        ordering = ['username']


class Post(models.Model):
    """
    博文模型
    """
    title = models.CharField(max_length=100, verbose_name=u'标题')
    summary = models.CharField(max_length=200, blank=True, verbose_name=u'摘要')
    body = models.TextField(verbose_name=u'正文')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_time = models.DateTimeField(verbose_name=u'编辑时间')
    category = models.ForeignKey(Category, verbose_name=u'博文类别', on_delete=False)
    tags = models.ManyToManyField(Tag, verbose_name=u'博文标签')
    author = models.ForeignKey(User, verbose_name=u'作者', on_delete=True)
    views = models.PositiveIntegerField(default=0)
    picture = models.ImageField(upload_to='media/post_img/%Y/%m', default='images/text02.jpg',
                                max_length=100, verbose_name=u'文章配图')

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        重写save方法，使其可以自动获取摘要
        :return: 无
        """
        if not self.summary:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.summary = strip_tags(md.convert(self.body))[:50]

        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'博文'
        verbose_name_plural = u'博文'
        ordering = ['-create_time']


class Source(Post):
    share_url = models.URLField(max_length=200, verbose_name=u'资源下载链接', blank=True, null=True)

    class Meta:
        verbose_name = u'资源分享'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
