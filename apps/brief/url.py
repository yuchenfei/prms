from django.conf.urls import url

from brief import views

urlpatterns = [
    url(r'^postgraduate/brief/list$', views.brief_list_p, name='brief_list_p'),
    url(r'^postgraduate/brief/new$', views.new, name='brief_new'),
    url(r'^postgraduate/brief/(\d+)/edit$', views.edit, name='brief_edit'),
    url(r'^postgraduate/brief/(\d+)/review$', views.review, name='brief_review_p'),

    url(r'^teacher/brief/list$', views.brief_list_t, name='brief_list_t'),
    url(r'^teacher/brief/(\d+)/review$', views.review, name='brief_review_t'),
]
