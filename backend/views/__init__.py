# -*- coding: utf8 -*-

"Import views"

from .login import login_user, logout_user
from .namespace import namespace_list, namespace_create
from .variable import (
    groups_list,
    group_create,
    group_delete,
    group_update,

    types_list,

    variables_list,
    variables_all,
    variable_create,
    variable_delete,
    variable_update
)
from .workflow import (
    workflows_list,
    workflows_create,

    layers_list,
    layers_create,
    layers_move,
    layers_delete,

    workflow_log
)
from .filters import (
    filters_list,
    filter_create,
    filter_move,
    filter_delete,

    filters_types,
    filter_configure,

    filter_link,
    link_delete
)
