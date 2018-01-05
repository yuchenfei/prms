from django.conf.urls import url

from leave import views

urlpatterns = [
    url(r'^teacher/leave_list', views.leave_list, name='leave_list'),
    url(r'^postgraduate/ask_for_leave$', views.ask_for_leave, name='ask_for_leave'),
]
