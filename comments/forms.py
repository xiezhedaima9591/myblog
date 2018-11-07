#-*- coding:utf-8 -*-
"""
    filename:       forms.py
    description:    django learning practice
    author:         xiezh
    date:           2018/11/2
"""
__author__ = 'xiezh'

from django import forms
from .models import Comment, Content


class CommentForm(forms.ModelForm):
    """
    文章评论表单
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']


class ContentForm(forms.ModelForm):
    """
    留言评论表单
    """
    class Meta:
        model = Content
        fields = ['name', 'email', 'text']