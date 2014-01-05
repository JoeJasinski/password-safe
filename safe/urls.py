from django.conf.urls import patterns, include, url
from safe.views import (AddKeyIndexView, AddKeyView, 
                        AddCredentialIndexView, AddCredentialView,
                        ListCredentialView, DetailCredentialView, ViewCredentialView)

urlpatterns = patterns('',

    url(r'^key/add/$', AddKeyIndexView.as_view(), {}, name="safe-key"),
    url(r'^key/add.json$', AddKeyView.as_view(), {}, name="safe-key-add"),
    url(r'^credential/$', ListCredentialView.as_view(), {}, name="safe-credential-list"),
    url(r'^credential/add/$', AddCredentialIndexView.as_view(), {}, name="safe-credential-add"),
    url(r'^credential/add.json$', AddCredentialView.as_view(), {}, name="safe-credential-add-json"),
    url(r'^credential/(?P<slug>[-_\w]+)/$', DetailCredentialView.as_view(), name='safe-credential-edit'),
    url(r'^credential/(?P<slug>[-_\w]+)\.json$', ViewCredentialView.as_view(), name='safe-credential-view-json'),
)
