import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from safe.models import PublicKey, Credential
from safe.forms import AddPublicKeyForm, AddCredentialForm


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        return json.dumps(context)


class AddKeyIndexView(TemplateView):
    template_name="safe/addkey.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddKeyIndexView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        return_value = super(AddKeyIndexView, self).get_context_data(**kwargs)
        domain = Site.objects.get_current().domain
        return_value['url_key_add'] = reverse('safe-key-add')
        return return_value
    

class AddKeyView(JSONResponseMixin, TemplateView):
    http_method_names = ['post',]
    form_class = AddPublicKeyForm

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddKeyView, self).dispatch(*args, **kwargs)
    
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        context = {}
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = request.user 
            key, created = PublicKey.objects.get_or_create(user=user)
            key.text = form.cleaned_data['pubkey']
            key.save()
            context.update({'message':"Key Added", 'pubkey':key.text})
        else:
            context.update({'errors':form.errors})
        return self.render_to_response(context)


class AddCredentialIndexView(TemplateView):
    template_name="safe/addcredential.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddCredentialIndexView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        return_value = super(AddCredentialIndexView, self).get_context_data(**kwargs)
        domain = Site.objects.get_current().domain
        return_value['form'] = AddCredentialForm()
        return_value['url_credential_add'] = reverse('safe-credential-add-json')
        return return_value


class AddCredentialView(JSONResponseMixin, TemplateView):
    
    http_method_names = ['post',]
    form_class = AddCredentialForm
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddCredentialView, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        context = {}
        form = self.form_class(data=request.POST)
        if form.is_valid():
            encrypted_secret = form.cleaned_data['secret']
            credential = form.save()
            credential.get_or_create_encrypted_usersecret(request.user, encrypted_secret)
            #cred  = Credential.objects.create_credential(name, slug)
            context.update({'message':"Credential Added",})
        else:
            context.update({'errors':form.errors})
        return self.render_to_response(context)


class ListCredentialView(ListView):
    http_method_names = [u'get',]
    template_name = "safe/listcredential.html"

    def get_queryset(self):
        return Credential.objects.get_user_credentials(user=self.request.user)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListCredentialView, self).dispatch(*args, **kwargs)
    