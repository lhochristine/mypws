from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'mainfests', ManifestViewSet, base_name='manifests')
router.register(r'manifestsshallow', ManifestShallowViewSet, base_name='manifestsshallow')
router.register(r'artifacts', ArtifactViewSet, base_name='artifacts')

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^manifestslist', manifests_index, name='manifests-list'),
    url(r'^api-json/', include(router.urls)),
    url(r'^manifest/(?P<pk>\d+)/artifactslist', artifacts_list, name='artifacts_list'),

    url(r'^duplicate/(?P<pk>\d+)$', manifest_duplicate, name='manifest_duplicate'),
    url(r'^delete/(?P<pk>\d+)$', manifestDelete.as_view(), name='manifest_delete'),
    url(r'^update/(?P<pk>\d+)$', manifestUpdate.as_view(), name='manifest_update'),
    url(r'^success_update', success_update, name='success_update'),
]