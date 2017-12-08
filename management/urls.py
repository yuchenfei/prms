from django.conf.urls import url

from management import views

urlpatterns = [
    url(r'^choose_login_type$', views.choose_login_type, name='choose_login_type'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^teacher/login$', views.login, name='teacher_login'),
    url(r'^teacher/$', views.teacher_home, name='teacher_home'),
    url(r'^teacher/postgraduates$', views.postgraduate_list, name='postgraduate_list'),
    url(r'^teacher/table_postgraduate_list$', views.table_postgraduate_list, name='table_postgraduate_list'),
    url(r'^teacher/import_postgraduate_list$', views.import_postgraduate_list, name='import_postgraduate_list'),
    url(r'^teacher/table_uploaded_postgraduate_list$', views.table_uploaded_postgraduate_list,
        name='table_uploaded_postgraduate_list'),
    url(r'^postgraduate/login$', views.login, name='postgraduate_login'),
    url(r'^postgraduate/$', views.postgraduate_home, name='postgraduate_home'),
    url(r'^check_in$', views.check_in, name='check_in'),
    url(r'^show_check_in$', views.show_check_in, name='show_check_in'),
]
