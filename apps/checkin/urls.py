from django.conf.urls import url

from checkin import views

urlpatterns = [
    url(r'^teacher/show_check_in$', views.show_check_in, name='show_check_in'),
    url(r'^check_in/temp_list$', views.temp_list, name='check_in_temp_list'),
    url(r'^check_in/temp_setting$', views.temp_setting, name='check_in_temp_setting'),
    url(r'^check_in/daily_setting$', views.daily_setting, name='check_in_daily_setting'),
    url(r'^check_in$', views.check_in, name='check_in'),
    url(r'^computer/list$', views.computer_list, name='computer_list'),
    url(r'^computer/add$', views.computer_add, name='computer_add'),
]
