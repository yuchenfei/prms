from django.conf.urls import url

from group_file import views

urlpatterns = [
    url(r'^teacher/group_file/list$', views.group_file_list, name='group_file_list'),
    url(r'^teacher/group_file/upload$', views.group_file_upload, name='group_file_upload'),
]
