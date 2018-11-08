"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('tag_list/<int:tag_id>/', views.TagView.as_view(), name='tag-post-list'),
    path('category_list/<int:category_id>/', views.CategoryView.as_view(), name='category-post-list'),
    path('date_list/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive-post-list'),
    path('about/<int:pk>', views.AboutMeDetailView.as_view(), name='about-me'),
    path('source_list/', views.SourceListView.as_view(), name='source-share'),
    path('search/', views.search, name='simple-search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
