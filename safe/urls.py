from django.conf.urls import patterns, include, url
from safe.views import AddKeyIndexView, AddKeyView, AddCredentialIndexView, AddCredentialView

urlpatterns = patterns('',

    url(r'^key/$', AddKeyIndexView.as_view(), {}, name="safe-key"),
    url(r'^key/add/$', AddKeyView.as_view(), {}, name="safe-key-add"),
    url(r'^secret/$', AddCredentialIndexView.as_view(), {}, name="safe-credential"),
    url(r'^secret/add/$', AddCredentialView.as_view(), {}, name="safe-credential-add"),
)
