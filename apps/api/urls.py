from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^auth$', views.auth, name='api_auth'),
    url(r'^check_in/items$', views.items, name='api_check_in_items'),
    url(r'^check_in$', views.check_in, name='api_check_in'),
]
