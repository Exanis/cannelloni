# -*- coding: utf8 -*-

"Serializers for namespace"

from rest_framework import serializers
from backend import models

class NamespaceSerializer(serializers.ModelSerializer):
    "Serializer for a namespace model"

    class Meta:
        model = models.Namespace
        fields = ('uuid', 'name',)
