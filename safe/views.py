import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from safe.models import PublicKey 
from safe.forms import AddPublicKeyForm


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        return json.dumps(context)


class IndexView(TemplateView):
    template_name = "index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        return_value = super(IndexView, self).get_context_data(**kwargs)
        domain = Site.objects.get_current().domain
        return_value['url_key_add'] = reverse('safe-key-add')
        return return_value
    

class AddKeyView(JSONResponseMixin, TemplateView):
    http_method_names = ['post',]

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddKeyView, self).dispatch(*args, **kwargs)
    
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        context = {}
        form = AddPublicKeyForm(data=request.POST)
        if form.is_valid():
            user = request.user 
            key, created = PublicKey.objects.get_or_create(user=user)
            key.text = form.cleaned_data['pubkey']
            key.save()
            context.update({'pubkey':key.text})
        else:
            context.update({'errors':form.errors})
        return self.render_to_response(context)
