#-*- coding:utf-8 -*-
"""
    filename:       blog_tags
    description:    博客自定义标签
    author:         xiezh
    date:           2018/10/31
"""
__author__ = 'xiezh'

from django import template
from django.db.models.aggregates import Count
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from ..models import User, Tag, Post, Category

register = template.Library()


@register.simple_tag
def get_web_about_info():
    """
    获取about需要的信息
    :return: 用户名为admin的信息
    """
    return User.objects.get(username='admin')


@register.simple_tag
def get_tags():
    """
    获取现有文章所有标签
    :return: 现有文章所有标签
    """
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def archives():
    """
    获取现有文章日期
    :return: 现有文章所有创建年份和月份
    """
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_category():
    """
    获取现有文章所有分类
    :return: 现有文章所有分类
    """
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_recent_post():
    """
    获取最近几篇文章
    :return: 最近5篇文章列表
    """
    return Post.objects.all()[:5]


@register.simple_tag
def get_pre_post(current_pk):
    """
    获取当前文章的上一篇
    :param current_pk: 当前文章id
    :return: 上一篇文章的post
    """
    try:
        post = Post.objects.get(id=current_pk - 1)
    except ObjectDoesNotExist:
        post = None
    return post


@register.simple_tag
def get_aft_post(current_pk):
    """
    获取当前文章的下一篇
    :param current_pk: 当前文章id
    :return: 下一篇文章的post
    """
    try:
        post = Post.objects.get(id=current_pk + 1)
    except ObjectDoesNotExist:
        post = None
    return post


@register.simple_tag
def get_relative_post(current_post):
    """
    获取当前文章相关文章列表
    :param current_post: 当前文章
    :return: 相关文章列表
    """
    return Post.objects.filter(Q(tags__name=current_post.tags.name)|Q(category=current_post.category))\
            .distinct()\
            .exclude(id=current_post.id)[:8]
