from django.conf.urls import patterns, include, url

from .views import CheckPersonView


urlpatterns = patterns('',
    url(r'^check/$', CheckPersonView.as_view(), name='check_person'),
)
