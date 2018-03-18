from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.branch_list, name='branch_list')
]