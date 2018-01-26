from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^auth$', views.auth, name='api_auth'),
]
