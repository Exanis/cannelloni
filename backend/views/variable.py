# -*- coding: utf8 -*-

"Variables-related views"

from rest_framework.decorators import api_view
from rest_framework.response import Response
from guardian.shortcuts import get_perms
from django.shortcuts import get_object_or_404
from backend import serializers, models

@api_view(['GET'])
def groups_list(request, uuid):
    "List all variables groups in specified namespace"
    namespace = get_object_or_404(models.Namespace, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, namespace):
        serialized = serializers.GroupSerializer(namespace.groups, many=True)
        return Response(serialized.data)
    return Response([])

@api_view(['GET'])
def variables_list(request, uuid):
    "List all variables in a specified group"
    group = get_object_or_404(models.Group, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, group.namespace):
        serialized = serializers.VariableSerializer(group.variables, many=True)
        return Response(serialized.data)
    return Response([])

@api_view(['GET'])
def variables_all(request, uuid):
    "List all variables in a specified namespace"
    namespace = get_object_or_404(models.Namespace, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, namespace):
        variables = models.Variable.objects.filter(group__namespace=namespace)
        serialized = serializers.VariableSerializer(variables, many=True)
        return Response(serialized.data)
    return Response([])

@api_view(['GET'])
def types_list(_):
    "List all availables types"
    types = models.Type.objects.all()
    serialized = serializers.TypeSerializer(types, many=True)
    return Response(serialized.data)

@api_view(['POST'])
def group_create(request, uuid):
    "Create a new group in a namespace"
    namespace = get_object_or_404(models.Namespace, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, namespace):
        name = request.POST['name']
        models.Group.objects.create(namespace=namespace, name=name)
        return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
def variable_create(request, uuid):
    "Create a new variable in a group"
    group = get_object_or_404(models.Group, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, group.namespace):
        name = request.POST['name']
        type_class = get_object_or_404(models.Type, slug=request.POST['type'])
        models.Variable.objects.create(group=group, type_class=type_class, name=name)
        return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
def group_update(request, uuid):
    "Update a group name"
    group = get_object_or_404(models.Group, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, group.namespace):
        group.name = request.POST['name']
        group.save()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
def variable_update(request, uuid):
    "Update a variable"
    variable = get_object_or_404(models.Variable, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, variable.group.namespace):
        variable.set(request)
        return Response({'success': True})
    return Response({'success': False})

@api_view(['DELETE'])
def group_delete(request, uuid):
    "Delete a group"
    group = get_object_or_404(models.Group, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, group.namespace):
        group.delete()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['DELETE'])
def variable_delete(request, uuid):
    "Delete a variable"
    variable = get_object_or_404(models.Variable, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, variable.group.namespace):
        variable.delete()
        return Response({'success': True})
    return Response({'success': False})
