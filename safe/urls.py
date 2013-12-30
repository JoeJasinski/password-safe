from django.conf.urls import patterns, include, url
from safe.views import IndexView, AddKeyView

urlpatterns = patterns('',

    url(r'^key/$', IndexView.as_view(template_name="safe/index.html"), {}, name="safe-key"),
    url(r'^key/add/$', AddKeyView.as_view(), {}, name="safe-key-add"),

)
