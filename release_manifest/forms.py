from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Manifest, Artifact

from djangoformsetjs.utils import formset_media_js

class ManifestForm(ModelForm):
    class Media(object):
        js = formset_media_js + (
        )

    class Meta:
        model = Manifest
        fields = '__all__'

class ArtifactsForm(ModelForm):
    class Media(object):
        js = formset_media_js + (
        )

    class Meta:
        model = Artifact
        fields = '__all__'

class DeleteNewForm(ModelForm):
    class Meta:
        model = Manifest
        fields = []

ArtifactsFormSet = inlineformset_factory(Manifest, Artifact,
                    form = ArtifactsForm,
                    fields=('__all__'),
                    can_delete=False,
                    extra=1)