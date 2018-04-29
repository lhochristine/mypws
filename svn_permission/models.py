# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain

from django.db import models
from svn_permission.choices import *

# Create your models here.
class Branch(models.Model):
    branch_name = models.CharField(max_length=32, primary_key=True, default='turnk')
    class Meta:
        verbose_name_plural = "branches"
        ordering = ['-branch_name']
    def __unicode__(self):
        return self.branch_name
    def get_branch(self):
        if self.branch_name == 'trunk':
            return self.branch_name
        else:
            return 'branches/%s' % (self.branch_name)

class Repository(models.Model):
    repo_name = models.CharField(max_length=5, primary_key=True, choices=REPO_CHOICES)
    branches = models.ManyToManyField(Branch)
    class Meta:
        verbose_name_plural = "repositories"
    def __unicode__(self):
        return self.repo_name
    def get_reponame(self):
        return '%s-repo:/projects/' % (self.repo_name)

class Module(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.PROTECT)
    mod_name = models.CharField(max_length=128, choices=MODULE_CHOICES, unique=True)
    def __unicode__(self):
        return self.mod_name

class Group(models.Model):
    name = models.CharField(max_length=64, primary_key=True, choices=GROUP_CHOICES)
    def __unicode__(self):
        return self.name

class User(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    groups = models.ManyToManyField(Group)
    def __unicode__(self):
        return self.uid

class GroupPerm(models.Model):
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    permission = models.CharField(max_length=2, choices=PERM_CHOICES, default='r')
    class Meta:
        verbose_name = "Group Permission"
        verbose_name_plural = "Group Permissions"
    def __unicode__(self):
        return "@%s = %s" % (self.group, self.permission)

class PartitionTest(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    group_perm = models.ManyToManyField(GroupPerm)

    class Meta:
        unique_together = ('module','branch')

    def __unicode__(self):
        return "%s%s/%s" % (Module.objects.get(id=self.module.id).repo.get_reponame(), self.branch, self.module)

    def associated_repo(self):
        return "%s" % Module.objects.get(id=self.module.id).repo

    def get_group_perm(self):
        # want to list svnadmin/buildadmin/then-sort-others
        svnadmin = self.group_perm.all().filter(group='svnadmin')
        buildadm = self.group_perm.all().filter(group='buildadmin')
        rest = self.group_perm.all().exclude(group='svnadmin').exclude(group='buildadmin').order_by('group')

        sort_list = list(chain(svnadmin, buildadm, rest))
        print "sort_list %s" % sort_list
        return sort_list

