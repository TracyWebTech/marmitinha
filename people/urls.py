from django.conf.urls import patterns, include, url

from .views import CreatePersonView


urlpatterns = patterns('',
    url(r'^add/$', CreatePersonView.as_view(), name='add'),
)
