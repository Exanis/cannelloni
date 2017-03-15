# -*- coding: utf8 -*-

"Filters related views"

import inspect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from guardian.shortcuts import get_perms
from django.shortcuts import get_object_or_404
from django.db.models import Max
from backend import models, filters

@api_view(['GET'])
def filters_list(request, uuid):
    "List all filters in a given layer"
    layer = get_object_or_404(models.Layer, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, layer.workflow.namespace):
        return Response([
            {
                'uuid': fil.uuid,
                'name': fil.name,
                'target': fil.target,
                'configurations': [
                    {
                        'uuid': config.uuid,
                        'key': config.key,
                        'value': {
                            'name': config.value.name,
                            'value': config.value.value
                        }
                    } for config in fil.configurations
                ],
                'links': [
                    {
                        'uuid': link.uuid,
                        'from': link.origin_node,
                        'to_filter': link.target_filter.name,
                        'to_uuid': link.target_filter.uuid,
                        'to_node': link.target_node
                    } for link in fil.links
                ],
                'links_in': [
                    {
                        'uuid': link.uuid,
                        'from_filter': link.origin_filter.name,
                        'from_uuid': link.origin_filter.uuid,
                        'from_node': link.origin_node,
                        'to': link.target_node
                    } for link in fil.links_in
                ]
            } for fil in layer.filters
        ])
    return Response([])

@api_view(['GET'])
def filters_types(_):
    "List all available filters"
    possibilities = inspect.getmembers(filters, inspect.isclass)
    return Response([
        {
            'slug': fil[0],
            'name': fil[1].name,
            'description': fil[1].description,
            'node_in': fil[1].node_in,
            'node_out': fil[1].node_out,
            'parameters': fil[1].parameters
        } for fil in possibilities
    ])

@api_view(['POST'])
def filter_create(request, uuid):
    "Create a filter in a layer"
    layer = get_object_or_404(models.Layer, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, layer.workflow.namespace):
        name = request.POST['name']
        target = request.POST['target']
        weight = models.Filter.objects.filter(layer=layer).aggregate(Max('weight'))
        if weight['weight__max'] is not None:
            models.Filter.objects.create(
                name=name,
                target=target,
                weight=(weight['weight__max'] + 1),
                layer=layer
            )
        else:
            models.Filter.objects.create(
                name=name,
                target=target,
                weight=0,
                layer=layer
            )
        return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
def filter_move(request, uuid):
    "Move a filter"
    fil = get_object_or_404(models.Filter, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, fil.layer.workflow.namespace):
        if request.POST['direction'] == '0':
            other_filter = models.Filter.objects.filter(
                layer=fil.layer,
                weight__gt=fil.weight
            ).earliest('weight')
        else:
            other_filter = models.Filter.objects.filter(
                layer=fil.layer,
                weight__lt=fil.weight
            ).latest('weight')
        if other_filter is None:
            return Response({'success': False})
        tmp = other_filter.weight
        other_filter.weight = fil.weight
        fil.weight = tmp
        fil.save()
        other_filter.save()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['DELETE'])
def filter_delete(request, uuid):
    "Delete a filter"
    fil = get_object_or_404(models.Filter, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, fil.layer.workflow.namespace):
        fil.delete()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
def filter_configure(request):
    "Set a configuration for a filter"
    filter_uuid = request.POST['filter']
    fil = get_object_or_404(models.Filter, uuid=filter_uuid)
    if 'view_namespace' in get_perms(request.user, fil.layer.workflow.namespace):
        variable_uuid = request.POST['variable']
        variable = get_object_or_404(models.Variable, uuid=variable_uuid)
        if 'view_namespace' in get_perms(request.user, variable.group.namespace):
            target = getattr(filters, fil.target)
            key = request.POST['key']
            for param in target.parameters:
                if param['key'] == key:
                    if param['type'] == variable.type_class.slug:
                        models.Configuration.objects.create(target=fil, key=key, value=variable)
                        return Response({'success': True})
                    else:
                        return Response({'success': False}) # break loop
    return Response({'success': False})

@api_view(['POST'])
def filter_link(request):
    "Set a link between two filters"
    origin_filter_uuid = request.POST['origin_filter']
    target_filter_uuid = request.POST['target_filter']
    origin_filter = get_object_or_404(models.Filter, uuid=origin_filter_uuid)
    target_filter = get_object_or_404(models.Filter, uuid=target_filter_uuid)
    if 'view_namespace' in get_perms(request.user, origin_filter.layer.workflow.namespace)\
        and origin_filter.layer.workflow == target_filter.layer.workflow:
        origin_node = request.POST['origin_node']
        target_node = request.POST['target_node']
        try:
            link = models.Link.objects.get(target_filter=target_filter, target_node=target_node)
        except models.Link.DoesNotExist:
            models.Link.objects.create(
                origin_filter=origin_filter,
                origin_node=origin_node,
                target_filter=target_filter,
                target_node=target_node
            )
            return Response({'succes': True})
        link.origin_filter = origin_filter
        link.origin_node = origin_node
        link.save()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['DELETE'])
def link_delete(request, uuid):
    "Delete a link between filters"
    link = get_object_or_404(models.Link, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, link.origin_filter.layer.workflow.namespace):
        link.delete()
        return Response({'success': True})
    return Response({'success': False})
