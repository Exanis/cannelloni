# -*- coding: utf8 -*-

"Urls for backend"

from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^auth/login$', views.login_user),
    url(r'^auth/logout$', views.logout_user),

    url(r'^namespaces/list$', views.namespace_list),
    url(r'^namespaces/create$', views.namespace_create),

    url(r'^types/list$', views.types_list),

    url(r'^groups/list/(?P<uuid>[a-z0-9\-]+)$', views.groups_list),
    url(r'^groups/create/(?P<uuid>[a-z0-9\-]+)$', views.group_create),
    url(r'^groups/update/(?P<uuid>[a-z0-9\-]+)$', views.group_update),
    url(r'^groups/delete/(?P<uuid>[a-z0-9\-]+)$', views.group_delete),

    url(r'^variables/list/(?P<uuid>[a-z0-9\-]+)$', views.variables_list),
    url(r'^variables/all/(?P<uuid>[a-z0-9\-]+)$', views.variables_all),
    url(r'^variables/create/(?P<uuid>[a-z0-9\-]+)$', views.variable_create),
    url(r'^variables/update/(?P<uuid>[a-z0-9\-]+)$', views.variable_update),
    url(r'^variables/delete/(?P<uuid>[a-z0-9\-]+)$', views.variable_delete),

    url(r'^workflows/list/(?P<uuid>[a-z0-9\-]+)$', views.workflows_list),
    url(r'^workflows/create/(?P<uuid>[a-z0-9\-]+)$', views.workflows_create),

    url(r'^layers/list/(?P<uuid>[a-z0-9\-]+)$', views.layers_list),
    url(r'^layers/create/(?P<uuid>[a-z0-9\-]+)$', views.layers_create),
    url(r'^layers/move/(?P<uuid>[a-z0-9\-]+)$', views.layers_move),
    url(r'^layers/delete/(?P<uuid>[a-z0-9\-]+)$', views.layers_delete),

    url(r'^filters/list/(?P<uuid>[a-z0-9\-]+)$', views.filters_list),
    url(r'^filters/create/(?P<uuid>[a-z0-9\-]+)$', views.filter_create),
    url(r'^filters/move/(?P<uuid>[a-z0-9\-]+)$', views.filter_move),
    url(r'^filters/delete/(?P<uuid>[a-z0-9\-]+)$', views.filter_delete),
    url(r'^filters/types$', views.filters_types),
    url(r'^filters/configure$', views.filter_configure),

    url(r'^filters/link$', views.filter_link),
    url(r'^filters/unlink/(?P<uuid>[a-z0-9\-]+)$', views.link_delete),

    url(r'^workflows/run/(?P<uuid>[a-z0-9\-]+)$', views.workflow_run),
    url(r'^workflows/status/(?P<uuid>[a-z0-9\-]+)$', views.workflow_watch),
    url(r'^workflows/log/(?P<uuid>[a-z0-9\-]+)$', views.workflow_log),
]
