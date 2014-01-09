from django.conf.urls import patterns, include, url
from safe.views import (AddKeyIndexView, CreateKeyView, 
                        CreateCredentialIndexView, CreateUpdateCredentialView,
                        ListCredentialView, UpdateCredentialView, 
                        ViewCredentialSecretView, DeleteCredentialView,
                        ListTagsView)

urlpatterns = patterns('',

    url(r'^key/add/$', AddKeyIndexView.as_view(), {}, name="safe-key"),
    url(r'^key/add.json$', CreateKeyView.as_view(), {}, name="safe-key-add"),
    url(r'^credential/$', ListCredentialView.as_view(), {}, name="safe-credential-list"),
    url(r'^credential/add/$', CreateCredentialIndexView.as_view(), {}, name="safe-credential-add"),
    url(r'^credential/add.json$', CreateUpdateCredentialView.as_view(), {}, name="safe-credential-add-json"),
    url(r'^credential/(?P<slug>[-_\w]+)/$', UpdateCredentialView.as_view(), name='safe-credential-edit'),
    url(r'^credential/(?P<slug>[-_\w]+)\.json$', ViewCredentialSecretView.as_view(), name='safe-credential-secret-view-json'),
    url(r'^credential/(?P<slug>[-_\w]+)/edit.json$', CreateUpdateCredentialView.as_view(), name='safe-credential-edit-json'),
    url(r'^credential/(?P<slug>[-_\w]+)/delete/$', DeleteCredentialView.as_view(), name='safe-credential-delete'),
    url(r'^tags\.json$', ListTagsView.as_view(), name='safe-tags-list'),
)
