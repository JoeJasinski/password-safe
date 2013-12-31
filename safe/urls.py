from django.conf.urls import patterns, include, url
from safe.views import AddKeyIndexView, AddKeyView, AddCredentialView

urlpatterns = patterns('',

    url(r'^key/$', AddKeyIndexView.as_view(), {}, name="safe-key"),
    url(r'^key/add/$', AddKeyView.as_view(), {}, name="safe-key-add"),
    url(r'^secret/add/$', AddCredentialView.as_view(), {}, name="safe-secret-add"),
)
