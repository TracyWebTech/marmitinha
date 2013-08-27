from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'marmita.views.index', name='home'),
    # url(r'^marmita/', include('marmita.foo.urls')),
    url(r'^users/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'base/base.html'}, name='login'),
    url(r'^users/', include('django.contrib.auth.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
