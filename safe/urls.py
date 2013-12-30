from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from safe.views import IndexView

urlpatterns = patterns('',

    (r'^$', IndexView.as_view(template_name="safe/index.html")),

)
