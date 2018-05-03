from django.conf.urls import url

from leave import views

urlpatterns = [
    url(r'^postgraduate/leave/new', views.ask_for_leave, name='ask_for_leave'),
    url(r'^postgraduate/leave/list', views.list_list_p, name='leave_list_p'),
    url(r'^teacher/leave/list$', views.leave_list_t, name='leave_list_t'),
    url(r'^teacher/leave/(\d+)/process$', views.processes_leave, name='processes_leave'),
]
