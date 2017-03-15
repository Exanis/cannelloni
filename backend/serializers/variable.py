# -*- coding: utf8 -*-

"Serializers for variables"

from rest_framework import serializers
from backend import models

class TypeSerializer(serializers.ModelSerializer):
    "Serializer for a type model"

    class Meta:
        model = models.Type
        fields = ('id', 'name', 'slug', 'container', 'icon',)

class GroupSerializer(serializers.ModelSerializer):
    "Serializer for a group model"

    class Meta:
        model = models.Group
        fields = ('uuid', 'namespace', 'name',)

class VariableSerializer(serializers.ModelSerializer):
    "Serializer for a variable model"

    class Meta:
        model = models.Variable
        fields = ('uuid', 'group', 'type_class', 'type_slug', 'parent', 'name', 'value',)
