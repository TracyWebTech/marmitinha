from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import CheckPersonView, UncheckPersonView, ChangeDateView, ChangeTicketView


urlpatterns = patterns('',
    url(r'^check/$', login_required(CheckPersonView.as_view()),
        name='check_person'),
    url(r'^uncheck/$', login_required(UncheckPersonView.as_view()),
        name='uncheck_person'),
    url(r'^change/$', login_required(ChangeDateView.as_view()),
        name='change'),
    url(r'^ticket/$', login_required(ChangeTicketView.as_view()),
        name='change_ticket'),
)
