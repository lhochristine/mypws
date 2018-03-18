# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Branch

# Create your views here.
def branch_list(request):
    branches = Branch.objects.order_by('branch_name').reverse()
    return render(request, 'svn_permission/svn_data.html', {'branches':branches})