#-*- coding:utf-8 -*-
"""
    filename:       feeds.py
    description:    django learning practice
    author:         xiezh
    date:           2018/11/7
"""
__author__ = 'xiezh'

from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    title = u"博客文章更新"

    link = "/"

    description = u"尹广超博客文章更新了"

    def items(self):
        return Post.objects.all()[:10]

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
