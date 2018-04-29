from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.branch_list, name='branch_list'),
    #url(r'^index/$', TemplateView.as_view(template_name='svn_permission/b_index.html')),
    url(r'^index/$', views.index),
    url(r'^contact/$', TemplateView.as_view(template_name='svn_permission/contact.html')),
    url(r'^svn_contact/$', views.svn_contact),
    url(r'^branches/(?P<branch_name>\D+)/$', views.branch_detail),
    #url(r'^branches/(?P<branch_name>\D+)/', TemplateView.as_view(template_name='svn_permission/contact.html')),
    url(r'^branches/RB-(?P<branch_name>\d.\d.\d)', views.branch_detail),
    #url(r'^branches/RB-(?P<branch_name>)', TemplateView.as_view(template_name='svn_permission/contact.html')),

    url(r'^repos/(?P<repo_name>\w+)/$', views.repo_detail),
]