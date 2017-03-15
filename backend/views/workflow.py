# -*- coding: utf8 -*-

"Namespace related views"

import os
from uuid import uuid4
from subprocess import Popen
from rest_framework.decorators import api_view
from rest_framework.response import Response
from guardian.shortcuts import get_perms
from django.shortcuts import get_object_or_404
from django.db.models import Max
from backend import serializers, models
from cannelloni import settings

@api_view(['GET'])
def workflows_list(request, uuid):
    "List all workflows for a given namespace"
    namespace = get_object_or_404(models.Namespace, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, namespace):
        serializer = serializers.WorkflowSerializer(namespace.workflows, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['POST'])
def workflows_create(request, uuid):
    "Create a new workflow in a namespace"
    namespace = get_object_or_404(models.Namespace, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, namespace):
        name = request.POST['name']
        models.Workflow.objects.create(name=name, namespace=namespace)
        return Response({'success': True})
    return Response({'success': False})

@api_view(['GET'])
def layers_list(request, uuid):
    "List all layers for a given workflow"
    workflow = get_object_or_404(models.Workflow, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, workflow.namespace):
        serializer = serializers.LayerSerializer(workflow.layers, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['POST'])
def layers_create(request, uuid):
    "Create a new layer in a namespace"
    workflow = get_object_or_404(models.Workflow, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, workflow.namespace):
        name = request.POST['name']
        weight = models.Layer.objects.filter(workflow=workflow).aggregate(Max('weight'))
        if weight['weight__max'] is not None:
            models.Layer.objects.create(
                workflow=workflow,
                name=name,
                weight=(weight['weight__max'] + 1)
            )
        else:
            models.Layer.objects.create(workflow=workflow, name=name, weight=0)
        return Response({'success': True})
    return Response({'success': False})

@api_view(['DELETE'])
def layers_delete(request, uuid):
    "Delete a layer"
    layer = get_object_or_404(models.Layer, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, layer.workflow.namespace):
        layer.delete()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
def layers_move(request, uuid):
    "Move a layer"
    layer = get_object_or_404(models.Layer, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, layer.workflow.namespace):
        if request.POST['direction'] == '0':
            other_layer = models.Layer.objects.filter(
                workflow=layer.workflow,
                weight__gt=layer.weight
            ).earliest('weight')
        else:
            other_layer = models.Layer.objects.filter(
                workflow=layer.workflow,
                weight__lt=layer.weight
            ).latest('weight')
        if other_layer is None:
            return Response({'success': False})
        tmp = other_layer.weight
        other_layer.weight = layer.weight
        layer.weight = tmp
        layer.save()
        other_layer.save()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['GET'])
def workflow_run(request, uuid):
    "Run a workflow"
    workflow = get_object_or_404(models.Workflow, uuid=uuid)
    if 'view_namespace' in get_perms(request.user, workflow.namespace):
        watch = uuid4()
        Popen([
            os.path.join(settings.BASE_DIR, 'run.sh'),
            str(uuid),
            str(watch)
        ])
        return Response({'watcher': watch})
    return Response({})

@api_view(['GET'])
def workflow_watch(_, uuid):
    "Watch the status of a workflow"
    filename = os.path.join(settings.BASE_DIR, "runner", "status", uuid)
    try:
        with open(filename, 'r') as pointer:
            line = pointer.readline()
            return Response({'status': line})
    except IOError:
        return Response({'status': 'Error'})

@api_view(['GET'])
def workflow_log(_, uuid):
    "Get the log file for a workflow"
    filename = os.path.join(settings.BASE_DIR, "runner", "status", "%s.log" % uuid)
    try:
        with open(filename, 'r') as pointer:
            return Response({'log': pointer.read().replace("\n", '<br />')})
    except IOError:
        return Response({'log': 'Workflow failed to start'})
