from django.conf.urls import url

from group_file import views

urlpatterns = [
    url(r'^group_file/list$', views.group_file_list, name='group_file_list'),
    url(r'^group_file/upload$', views.group_file_upload, name='group_file_upload'),
    url(r'^group_file/delete$', views.group_file_delete, name='group_file_delete'),
]
