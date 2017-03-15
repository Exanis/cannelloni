# -*- coding: utf8 -*-

"Serializers for workflow"

from rest_framework import serializers
from backend import models

class WorkflowSerializer(serializers.ModelSerializer):
    "Serializer for a workflow model"

    class Meta:
        model = models.Workflow
        fields = ('uuid', 'namespace', 'name',)

class LayerSerializer(serializers.ModelSerializer):
    "Serializer for a layer model"

    class Meta:
        model = models.Layer
        fields = ('uuid', 'workflow', 'name', 'weight',)
