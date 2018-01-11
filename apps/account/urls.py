from django.conf.urls import url

from account import views

urlpatterns = [
    url(r'^$', views.home, name='home'),  # 主页选择登陆类型
    url(r'^logout$', views.logout, name='logout'),  # 登出
    url(r'^teacher/login$', views.login, name='teacher_login'),  # 教师登陆
    url(r'^teacher/$', views.teacher_home, name='teacher_home'),

    url(r'^teacher/manage_group_teacher$', views.manage_group_teacher, name='manage_group_teacher'),
    # url(r'^teacher/import_teacher', views.import_teacher, name='import_teacher'),

    url(r'^teacher/postgraduates$', views.postgraduate_list, name='postgraduate_list'),
    url(r'^teacher/table_postgraduate_list$', views.table_postgraduate_list, name='table_postgraduate_list'),

    url(r'^teacher/import_postgraduate_list$', views.import_postgraduate_list, name='import_postgraduate_list'),
    url(r'^teacher/table_uploaded_postgraduate_list$', views.table_uploaded_postgraduate_list,
        name='table_uploaded_postgraduate_list'),

    url(r'^teacher/import_teacher$', views.import_teacher, name='import_teacher'),
    url(r'^teacher/table_uploaded_teacher_list$', views.table_uploaded_teacher_list,
        name='table_uploaded_teacher_list'),

    url(r'^postgraduate/login$', views.login, name='postgraduate_login'),  # 研究生登陆
    url(r'^postgraduate/$', views.postgraduate_home, name='postgraduate_home'),
]
