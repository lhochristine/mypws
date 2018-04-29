# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

from .models import *

# Create your views here.
def branch_list(request):
    branches = Branch.objects.all()
    repos = Repository.objects.all()
    return render(request, 'svn_permission/svn_data.html', {'branches':branches, 'repos':repos})

def svn_contact(request):
    return render(request, 'svn_permission/b_index.html')

def gohome(request):
    return HttpResponsePermanentRedirect(reverse('base'))

def index(request):
    branches = Branch.objects.all()
    repos = Repository.objects.all()
    return render(request, 'svn_permission/b_index.html', {'branches':branches})


def branch_detail(request, branch_name):
    print ("input branch_number %s" % branch_name)
    if branch_name != 'trunk':
        pk = 'RB-' + branch_name
    else:
        pk = branch_name
    print ("pk %s" % pk)
    branch = get_object_or_404(Branch, pk=pk)
    branches = Branch.objects.all() # used for sidebar

    repos = Repository.objects.all() # used for sidebar
    repo_set = Repository.objects.filter(branches=pk)
    print ("repo.filter [%s]" % repo_set)

    parts = PartitionTest.objects.filter(branch=pk)
    parts[0].get_group_perm()
    #mods_list = []
    #for r in repo_set.iterator():
    #    print "r[%s]" % r
    #    mods_list.extend(list(Module.objects.filter(repo=r)))
    #    print "mods [%d][%s]" % (mods_list.__len__(), mods_list)
    #    for m in mods_list:
    #        part = PartitionTest.objects.filter(module=m)
    #        print "part [%s] group[%s]" % (part, part.values('group'))



    #user = User.objects.get(groups=parts.values('group'))
    #print "user [%s]" % user
    #groups = user.groups.all()

    return render(request, 'svn_permission/b_detail.html',
                 # {'branches':branches, 'repos':repos, 'branch':branch, 'repo':repo_set, 'mods':mods_list, 'groups':groups, 'users':user, 'parts': parts})
                  {'branches':branches, 'repos':repos, 'branch':branch, 'repo':repo_set, 'parts': parts})

def repo_detail(request, repo_name):
    print ("input repo_name %s" % repo_name)
    repo = Repository.objects.get(repo_name=repo_name)
    branch_set = repo.branches.all()
    print ("associated branches %s" % branch_set)
    return render(request, 'svn_permission/r_detail.html', {'branches':Branch.objects.all(), 'repos':Repository.objects.all(), 'branch_set':branch_set, 'repo': repo})

def repo_detail2(request, repo_name):
    print ("input repo_name %s" % repo_name)
    #if branch_name == 'trunk':
    #    branch = get_object_or_404(Branch, pk=branch_name)
    branches = Branch.objects.all()
    repos = Repository.objects.all()
    return render(request, 'svn_permission/r_detail.html', {'branches':branches, 'repos':repos,'repo':repo_name})
