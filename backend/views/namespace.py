# -*- coding: utf8 -*-

"Namespace related views"

from rest_framework.decorators import api_view
from rest_framework.response import Response
from guardian.shortcuts import get_objects_for_user, assign_perm
from backend import serializers, models

@api_view(['GET'])
def namespace_list(request):
    "List all namespace for the current user"
    objects = get_objects_for_user(request.user, 'backend.view_namespace')
    serializer = serializers.NamespaceSerializer(objects, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def namespace_create(request):
    "Create a new namespace and grant rights to it for user"
    name = request.POST['name']
    namespace = models.Namespace.objects.create(name=name)
    assign_perm('view_namespace', request.user, namespace)
    return Response({'success': True})
