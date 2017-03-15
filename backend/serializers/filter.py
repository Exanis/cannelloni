# -*- coding: utf8 -*-

"Serializers for filters"

from rest_framework import serializers
from backend import models

class FilterSerializer(serializers.ModelSerializer):
    "Serializer for a filter model"

    class Meta:
        model = models.Filter
        fields = ('uuid', 'layer', 'name', 'target', 'weight',)

class ConfigurationSerializer(serializers.ModelSerializer):
    "Serializer for a configuration model"

    class Meta:
        model = models.Configuration
        fields = ('uuid', 'target', 'key', 'value',)

class LinkSerializer(serializers.ModelSerializer):
    "Serializer for a link model"

    class Meta:
        model = models.Link
        fields = (
            'uuid',
            'origin_filter',
            'origin_node',
            'target_filter',
            'target_node',
        )
