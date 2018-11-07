# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.urls import reverse

from .models import Comment, Content
from .forms import  CommentForm, ContentForm

# Create your views here.


def post_comment(request, post_pk):
    """
    提交评论
    :param request:
    :param post_pk: 正在评论的文章ID
    :return: 无
    """
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)

    return redirect(post)


def post_content(request):
    """
    提交留言
    :param request:
    :return: 无
    """
    if request.method == 'POST':
        form = ContentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('comments:post-content'))
        else:
            return render(request, 'blog/contact.html', {'form': form})

    form = ContentForm()

    return render(request, 'blog/contact.html', {'form': form})
