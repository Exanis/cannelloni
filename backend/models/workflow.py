# -*- coding: utf8 -*-

"Workflow related variables"

from uuid import uuid4
from django.db import models

class Workflow(models.Model):
    "A workflow"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    namespace = models.ForeignKey("backend.Namespace", related_name="workflows_relation")
    name = models.CharField(max_length=255)

    @property
    def layers(self):
        "Iterable list of all layers in this workflow"
        return self.layers_relation.all()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Layer(models.Model):
    "A layer is a group of filter in a workflow"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    workflow = models.ForeignKey("backend.workflow", related_name="layers_relation")
    name = models.CharField(max_length=255, default="New layer")
    weight = models.IntegerField(default=0)

    @property
    def filters(self):
        "Iterable list of all filters in this layer"
        return self.filters_relation.all()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['weight']
