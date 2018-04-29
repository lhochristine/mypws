# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
#import requests
import os

# Create your models here.
VENDOR_CHOICES = (
    (None, 'Select:'),
    ('pws', 'pws'),
    ('pws_3rdp', 'pws 3rpd'),
    ('thirdp', 'thirdp')
)

BUILD_CHOICES = (
    (None, 'Select:'),
    ('FullBuild', 'Full Build'),
    ('opstools', 'opstools'),
    ('ansible', 'ansible'),
    ('None', 'None')
)

SW_TYPE_CHOICES = (
    ('PROD', 'Production'),
    ('OPS', 'Operations')
)

class Manifest(models.Model):
    release = models.CharField(max_length=30, default="")
    revision = models.CharField(max_length=30, default="")
    date_added = models.DateTimeField(auto_now=True)
    ext_release = models.CharField(max_length=30, default="", null=True, blank=True)
    sw_type = models.CharField(choices=SW_TYPE_CHOICES, max_length=30, default="PROD", blank=True)

    class Meta:
        unique_together = ('release', 'revision')

    def __str__(self):
        return self.release + "-" + self.revision


class Artifact(models.Model):
    parent_manifest = models.ForeignKey(Manifest, related_name='artifacts')
    name = models.CharField(max_length=200, default="")
    group = models.CharField(max_length=30, default="")
    version = models.CharField(max_length=200, default="")
    vendor = models.CharField(choices=VENDOR_CHOICES, default=None, max_length=30)
    var_name = models.CharField(max_length=30, default="")
    built_by = models.CharField(choices=BUILD_CHOICES, default=None, max_length=30)
    date_added = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=100, default="", blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('parent_manifest', 'name', 'group')

    def __str__(self):
        return self.name

@receiver(post_save, sender=Manifest, dispatch_uid="DeleteOldManifest")
def DeleteOldManifest(sender, instance, raw=False, **kwargs):
    if "RC" in instance.revision.upper() or "FINAL" in instance.revision.upper() :
        manlist = Manifest.objects.all()
        keep_date = timezone.now() - timedelta(days=10)

        skippedFirst = False
        for m in sorted(manlist, key=lambda x: x.date_added, reverse=True):
            if skippedFirst and (m.date_added is None or m.date_added < keep_date):
                m.delete()
            else:
                skippedFirst = True

        print("about to kick off the jenkins job")

        # these environment vars are read in by httpd from /etc/sysconfig/httpd when papriqa starts
        # commented out because we don't have Jenkins setup
        #jenkins_host_port = os.environ['jenkins_host_port']
        #builduser = os.enviorn['builduser']
        #buildpass = os.enviorn['buildpass']
        #url = jenkins_host_port + "/job/Save_to_release_candidate_repo/buildWithParameters?release=" + instance.release + "&revision=" + instance.revision + "&token=paprqa"
        #print(url)
        #print(builduser)
        #r = requests.get(url, auth=(builduser, buildpass))
        #print(r.status_code)