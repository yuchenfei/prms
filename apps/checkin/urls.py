from django.conf.urls import url

from checkin import views

urlpatterns = [
    url(r'^teacher/show_check_in$', views.show_check_in, name='show_check_in'),
    url(r'^check_in/temp/list$', views.temp_list, name='check_in_temp_list'),
    url(r'^check_in/temp/new$', views.temp_new, name='check_in_temp_new'),
    url(r'^check_in/temp/(\d+)/delete$', views.temp_delete, name='check_in_temp_delete'),
    url(r'^check_in/daily/setting$', views.daily_setting, name='check_in_daily_setting'),
    url(r'^check_in/my_items', views.my_items, name='check_in_my_items'),
    url(r'^check_in$', views.check_in, name='check_in'),
    url(r'^check_in/status$', views.check_in_status, name='check_in_status'),
    url(r'^computer/list$', views.computer_list, name='computer_list'),
    url(r'^computer/new', views.computer_new, name='computer_new'),
    url(r'^computer/delete$', views.computer_delete, name='computer_delete')
]
