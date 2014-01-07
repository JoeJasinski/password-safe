import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

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

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

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

    def post(self, request, *args, **kwargs):
        context = {}
        form = self.form_class(data=request.POST)
        if form.is_valid():
            encrypted_secret = form.cleaned_data['secret']
            credential = form.save()
            credential.get_or_create_encrypted_usersecret(request.user, encrypted_secret)
            context.update({'message':"Credential Added",})
        else:
            context.update({'errors':form.errors})
        return self.render_to_response(context)


class CredentialOwnershipMixin(object):

    def get_queryset(self):
        return self.model._default_manager.get_user_credentials(user=self.request.user)

class ListCredentialView(CredentialOwnershipMixin, ListView):
    
    model = Credential
    http_method_names = [u'get',]
    template_name = "safe/listcredential.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListCredentialView, self).dispatch(*args, **kwargs)

    def get_context_object_name(self, obj):
        return "credentials"


class DetailCredentialView(CredentialOwnershipMixin, DetailView):
    
    model = Credential
    http_method_names = [u'get']
    template_name = "safe/editcredential.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailCredentialView, self).dispatch(*args, **kwargs)

    def get_context_object_name(self, obj):
        return "credential"


class ViewCredentialView(JSONResponseMixin, CredentialOwnershipMixin, DetailView):
    model = Credential
    http_method_names = [u'get']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return_value = super(ViewCredentialView, self).dispatch(*args, **kwargs)
        return return_value

    def get(self, request, *args, **kwargs):
        context = {'message':'Key returned', 
                   'encrypted_secret':self.get_object().get_usersecret_cyphertext(request.user)}
        return self.render_to_response(context)
    
    def get_context_object_name(self, obj):
        return "credential"


class DeleteCredentialView(CredentialOwnershipMixin, DeleteView):
    model = Credential
    http_method_names = [u'get', u'post']
    success_url = reverse_lazy('safe-credential-list')
    template_name = "safe/deletecredential.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return_value = super(DeleteCredentialView, self).dispatch(request, *args, **kwargs)
        return return_value

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        secret = self.object.get_usersecret(user=request.user)
        if secret:
            secret.delete()
            if not self.object.user_secrets.count():
                self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_object_name(self, obj):
        return "credential"
