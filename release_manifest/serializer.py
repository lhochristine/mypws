from django.contrib import admin
from django.contrib.auth.models import User
admin.autodiscover()

from rest_framework import serializers
from .models import Manifest, Artifact

class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = (
            'name',
            'group',
            'version',
            'var_name',
            'built_by',
            'date_added',
            'comment',
            'deleted'
        )

class ManifestShallowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manifest
        fields = '__all__'

class ManifestSerializer(serializers.ModelSerializer):
    artifacts = ArtifactSerializer(many=True)

    class Meta:
        model = Manifest
        fields = (
            'id',
            'release',
            'revision',
            'date_added',
            'ext_release',
            'sw_type',
            'artifacts'
        )
    def create(self, validated_data):
        artifacts_data = validated_data.pop('artifacts')
        manifest = Manifest.objects.create(**validated_data)
        for data in artifacts_data:
            Artifact.objects.create(parent_manifest=manifest, **data)

        return manifest