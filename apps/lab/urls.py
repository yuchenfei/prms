from django.conf.urls import url

from lab import views

urlpatterns = [
    url(r'^teacher/experiment/list', views.ex_list, name='ex_list'),
    url(r'^teacher/experiment/add', views.ex_add, name='ex_add'),
    url(r'^teacher/grade/list', views.grade_list, name='grade_list'),
    url(r'^teacher/grade/add', views.grade_add, name='grade_add'),
]
