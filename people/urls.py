from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import CreatePersonView


urlpatterns = patterns('',
    url(r'^add/$', login_required(CreatePersonView.as_view()), name='add'),
)
