# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Branch)
admin.site.register(Repository)
admin.site.register(Module)
admin.site.register(Group)
admin.site.register(User)
admin.site.register(GroupPerm)
admin.site.register(PartitionTest)