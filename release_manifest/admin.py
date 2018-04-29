# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Manifest, Artifact

# Register your models here.
class ArtifactInline(admin.StackedInline):
    model = Artifact
    extra = 1

class ManifestAdmin(admin.ModelAdmin):
    list_display = ['release', 'revision', 'date_added', 'ext_release']
    inlines = [ArtifactInline]
    save_as = True
    save_on_top = True

class ArtifactAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'version', 'vendor', 'var_name', 'built_by', 'date_added', 'parent_manifest', 'comment']
    save_on_top = True

admin.site.register(Manifest, ManifestAdmin)
admin.site.register(Artifact, ArtifactAdmin)
