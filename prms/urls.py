"""prms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from account import views as account_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # 管理后台
    url(r'^$', account_views.home, name='home'),  # 主页选择登陆类型
    url(r'^logout$', account_views.logout, name='logout'),  # 登出

    url(r'^teacher/login$', account_views.login, name='teacher_login'),  # 教师登陆
    url(r'^teacher/$', account_views.teacher_home, name='teacher_home'),
    url(r'^teacher/postgraduates$', account_views.postgraduate_list, name='postgraduate_list'),
    url(r'^teacher/table_postgraduate_list$', account_views.table_postgraduate_list, name='table_postgraduate_list'),
    url(r'^teacher/import_postgraduate_list$', account_views.import_postgraduate_list, name='import_postgraduate_list'),
    url(r'^teacher/table_uploaded_postgraduate_list$', account_views.table_uploaded_postgraduate_list,
        name='table_uploaded_postgraduate_list'),

    url(r'^postgraduate/login$', account_views.login, name='postgraduate_login'),  # 研究生登陆
    url(r'^postgraduate/$', account_views.postgraduate_home, name='postgraduate_home'),


]

# 上传文件需要开启
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
