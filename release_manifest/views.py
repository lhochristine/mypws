# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect


import rest_framework
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Manifest, Artifact
from .serializer import ManifestSerializer, ManifestShallowSerializer, ArtifactSerializer
from .forms import *

import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the release_manifest page")

class ManifestViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Manifest.objects.order_by('-date_added')
    serializer_class = ManifestSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['sw_type']

class ManifestShallowViewSet(ModelViewSet):
    queryset = Manifest.objects.order_by('-date_added')
    serializer_class = ManifestShallowSerializer
    filter_backends = (DjangoFilterBackend,)


class ArtifactViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer
    filter_backends = (DjangoFilterBackend,)
#    filter_fields = ('parent_manifest__release', 'parent_manifest__revision', 'name')

def manifests_index(request):
    return render(request, 'manifests/manifests_main.html')

def jsonize(request):
    manifests = Manifest.objects.order_by('-date_added')
    return HttpResponse(json.dumps(manifests), content_type='application/json')

def artifacts_list(request, pk):
    artifacts = get_object_or_404(Manifest, pk=pk)
    return render(request, 'manifests/manifest_artifacts.html', {'artifacts': artifacts})

# get manifest for duplicating
def manifest_duplicate(request, pk, tempate_name='manifests/manifest_duplicate.html'):
    print("Enter duplicate def")
    obj_to_copy = get_object_or_404(Manifest, pk=pk)
    ''' save sw type from source record for later use '''
    formSwtype = obj_to_copy.sw_type
    print ("formSwtype <%s>" %formSwtype)
    if 'save-as' in request.POST:
        print("SAVE-AS-NEW button clicked")
        artifacts_obj = obj_to_copy.artifacts
        fromRevision = obj_to_copy.revision
        form = ManifestForm(request.POST or None, instance=obj_to_copy)
        if form.is_valid():
            print ("In manifestDuplicate:FORM_IS_VALID(), obj_to_copy.sw_type<%s>" %obj_to_copy.sw_type)
            form_obj = form.save(commit=False)
            form_obj.pk = None
            """ for sw_type, we disabled input when duplicate the record, so will populate it with source value """
            form_obj.sw_type = formSwtype
            form_obj.save()
            obj_to_copy = get_object_or_404(Manifest, pk=pk)
            artifacts_obj = obj_to_copy.artifacts
            """ now copy the artifacts """
            for a in artifacts_obj.all():
                a.pk = None
                a.parent_manifest = form_obj
                a.save()

            template_vars = {'source': fromRevision, 'target': form_obj.revision, 'action': 'duplicated'}
            return render(request, 'manifests/success_duplicate.html', template_vars)
        else:
            print ("In manifestDuplicate:FORM_INVALID")
    elif 'save' in request.POST:
        print ("SAVE button clicked")
        fromRevision = obj_to_copy.revision
        form = ManifestForm(request.POST or None, instance=obj_to_copy)
        if form.is_valid():
            form_obj = form.save()
            template_vars = {'source': fromRevision, 'target': form_obj.revision, 'action': 'renamed'}
            return render(request, 'manifests/success_duplicate.html', template_vars)
    else:
        form = ManifestForm(initial={'release': obj_to_copy.release, 'revision': 'rc_', 'sw_type': obj_to_copy.sw_type})

    template_vars = {'form': form, 'manifest': obj_to_copy, 'orig': obj_to_copy}
    return render(request, 'manifests/manifest_duplicate.html', template_vars)

from django.views.generic import UpdateView, DeleteView
class manifestDelete(DeleteView):
    model = Manifest
    form_class = ManifestForm
    template_name = 'manifests/manifest_delete.html'
    def get(self, request, pk):
        obj_to_delete = get_object_or_404(self.model, pk=pk)
        context = {'form': self.form_class(instance=obj_to_delete), 'manifest': obj_to_delete}
        return render(request, self.template_name, context)

    def delete(self, request, pk):
        self.object = self.get_object()
        success_url = 'manifests/success_delete.html'
        self.object.delete()
        print ("The delete success url is <%s>\n" %success_url)
        return render(request, success_url, {'target': self.object.revision})

from django.db import transaction
class manifestUpdate(UpdateView):
    model = Manifest
    fields = ['release', 'revision', 'ext_release', 'sw_type']
    template_name = 'manifests/manifest_update.html'

    def get_success_url(self):
        self.success_url = '/release_manifest/success_update.html'
        return self.success_url

    def get_context_data(self, **kwargs):
        print ("In manifestUpdate: GET_CONTEXT_DATA()")
        context = super(manifestUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['artifacts_form'] = ArtifactsFormSet(self.request.POST, instance=self.object)
        else:
            context['manifest'] = self.object
            context['artifacts_form'] = ArtifactsFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        print ("In manifestUpdate: FORM_VALID()")
        context = self.get_context_data()
        artifacts = context['artifacts_form']
        with transaction.atomic():
            self.object = form.save()
            if artifacts.is_valid():
                artifacts.instance = self.object
                artifacts.save()

        print ("success_url %s" %self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print ("In manifestUpdate: FORM_INVALID()")
        return self.render_to_response(self.get_context_data(form=form))

def success_update(request):
    return render(request, 'manifests/success_update.html')