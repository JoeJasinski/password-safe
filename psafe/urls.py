from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'psafe.views.home', name='home'),
    url(r'^safe/', include('safe.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
