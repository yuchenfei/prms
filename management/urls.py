from django.conf.urls import url

from management import views

urlpatterns = [
    url(r'^choose_login_type$', views.choose_login_type, name='choose_login_type'),
    url(r'^teacher/login$', views.login, name='teacher_login'),
    url(r'^teacher/$', views.teacher_home, name='teacher_home'),
    url(r'^postgraduate/login$', views.login, name='postgraduate_login'),
]
