# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Branch(models.Model):
    branch_name = models.CharField(max_length=32, primary_key=True, default='turnk')

    class Meta:
        verbose_name_plural = "branches"

    def __unicode__(self):
        return self.branch_name
