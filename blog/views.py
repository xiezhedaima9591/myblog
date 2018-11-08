# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import render
from comments.forms import CommentForm
from .models import Post, User, Source
import markdown

# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        加上分页数据
        :param kwargs: 关键字参数
        :return: 加上分页数据的context
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        """
        根据需要生成分页数据
        :param paginator:
        :param page:
        :param is_paginated:
        :return: 生成好的分页数据
        """
        if not is_paginated:
            return {}

        # 当前页号左边的号码
        left = []

        # 当前页号右边的号码
        right = []

        # 标识第1页后是否显示省略号
        left_has_more = False

        # 标识最后一页前是否显示省略号
        right_has_more = False

        # 标识是否显示第一页
        first = False

        # 标识是否显示最后一页
        last = False

        # 获取当前页码
        page_number = page.number

        # 获取总页数
        total_pages = paginator.num_pages

        # 获取分页页码列表
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number: page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number -3) if (page_number - 3) > 0 else 0: page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            right = page_range[page_number: page_number + 2]

            if right[-1] < total_pages -1:
                right_has_more = True
            if left[0] > 2:
                left_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


class SourceListView(IndexView):
    model = Source


class AboutMeDetailView(DetailView):
    model = User
    queryset = User.objects.all()
    template_name = 'blog/about.html'
    context_object_name = 'about'


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extension=[
                                        'markdown.extension.extra',
                                        'markdown.extension.codehilite',
                                        'markdown.extension.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        post = self.get_object()
        comment_list = post.comment_set.all()
        context['form'] = form
        context['comment_list'] = comment_list
        return context


class TagView(ListView):
    template_name = "blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        """
        设置查询集为特定标签下的文章列表
        :return: 文章列表
        """
        post_list = Post.objects.filter(tags=self.kwargs['tag_id'])
        for post in post_list:
            post.body = markdown.markdown(post.body,
                                      extension=[
                                        'markdown.extension.extra',
                                        'markdown.extension.codehilite',
                                        'markdown.extension.toc',
                                      ])

        return post_list


class CategoryView(ListView):
    template_name = "blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        """
        设置查询集为特定类型下的文章列表
        :return: 文章列表
        """
        post_list = Post.objects.filter(category=self.kwargs['category_id'])
        for post in post_list:
            post.body = markdown.markdown(post.body,
                                          extension=[
                                              'markdown.extension.extra',
                                              'markdown.extension.codehilite',
                                              'markdown.extension.toc',
                                          ])

        return post_list


class ArchiveView(ListView):
    template_name = "blog/index.html"
    context_object_name = 'post_list'

    def get_queryset(self):
        """
        设置查询集为特定归档时间下的文章列表
        :return: 文章列表
        """
        post_list = Post.objects.filter(Q(create_time__year=self.kwargs['year'])
                                        & Q(create_time__month=self.kwargs['month']))
        for post in post_list:
            post.body = markdown.markdown(post.body,
                                          extension=[
                                              'markdown.extension.extra',
                                              'markdown.extension.codehilite',
                                              'markdown.extension.toc',
                                          ])

        return post_list


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = u'请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__contains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'post_list': post_list})
