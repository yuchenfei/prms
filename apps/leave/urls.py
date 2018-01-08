from django.conf.urls import url

from leave import views

urlpatterns = [
    url(r'^postgraduate/ask_for_leave$', views.ask_for_leave, name='ask_for_leave'),
    url(r'^teacher/leave_list$', views.leave_list, name='leave_list'),
    url(r'^teacher/processes_leave/(\d+)/$', views.processes_leave, name='processes_leave'),
]
