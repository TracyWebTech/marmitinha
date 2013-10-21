from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import CheckUncheckPersonView, ChangeDateView, ChangeTicketView


urlpatterns = patterns('',
    url(r'^check_uncheck/$', login_required(CheckUncheckPersonView.as_view()),
        name='check_uncheck_person'),
    url(r'^change/$', login_required(ChangeDateView.as_view()),
        name='change'),
    url(r'^ticket/$', login_required(ChangeTicketView.as_view()),
        name='change_ticket'),
)
