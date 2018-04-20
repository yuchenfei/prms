from django.conf.urls import url

from account import views

urlpatterns = [
    url(r'^$', views.home, name='home'),  # 主页选择登陆类型
    url(r'^logout$', views.logout, name='logout'),  # 登出
    url(r'^teacher/login$', views.login, name='teacher_login'),  # 教师登陆
    url(r'^teacher/$', views.teacher_home, name='teacher_home'),  # 教师首页
    url(r'^postgraduate/login$', views.login, name='postgraduate_login'),  # 研究生登陆
    url(r'^postgraduate/$', views.postgraduate_home, name='postgraduate_home'),  # 研究生首页
    url(r'^teacher/setting$', views.setting_t, name='setting_t'),  # 教师设置
    url(r'^postgraduate/setting$', views.setting_p, name='setting_p'),  # 研究生设置

    url(r'^teacher/group/members$', views.members, name='g_members'),  # 组成员列表
    url(r'^teacher/group/invite$', views.invite, name='g_invite'),  # 邀请教师入组
    url(r'^teacher/group/handle_invite/(\d+)/$', views.handle_invite, name='g_handle_invite'),  # 处理邀请
    url(r'^teacher/group/remove$', views.remove, name='g_remove'),  # 移出教师

    url(r'^teacher/postgraduates$', views.postgraduate_list, name='postgraduate_list'),  # 研究生列表页面
    url(r'^teacher/table_postgraduate_list$', views.table_postgraduate_list, name='table_postgraduate_list'),  # 研究生列表数据
    url(r'^teacher/postgraduates/add$', views.add_postgraduate, name='add_postgraduate'),

    # 导入研究生
    url(r'^teacher/import_postgraduate_list$', views.import_postgraduate_list, name='import_postgraduate_list'),
    # 导入研究生预览
    url(r'^teacher/table_uploaded_postgraduate_list$', views.table_uploaded_postgraduate_list,
        name='table_uploaded_postgraduate_list'),

    url(r'^teacher/import_teacher$', views.import_teacher, name='import_teacher'),  # 导入教师
    url(r'^teacher/table_uploaded_teacher_list$', views.table_uploaded_teacher_list,  # 导入教师预览
        name='table_uploaded_teacher_list'),
]
