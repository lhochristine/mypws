# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

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
    queryset = Manifest.objects.all()
    serializer_class = ManifestSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['sw_type']

class ManifestShallowViewSet(ModelViewSet):
    queryset = Manifest.objects.all()
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
    manifests = Manifest.objects.all()
    return HttpResponse(json.dumps(manifests), content_type='application/json')

def artifacts_list(request, pk):
    artifacts = get_object_or_404(Manifest, pk=pk)
    return render(request, 'manifests/manifest_artifacts.html', {'artifacts': artifacts})