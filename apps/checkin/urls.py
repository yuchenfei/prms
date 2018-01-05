from django.conf.urls import url

from checkin import views

urlpatterns = [
    url(r'^teacher/show_check_in$', views.show_check_in, name='show_check_in'),
    url(r'^check_in$', views.check_in, name='check_in'),
]
