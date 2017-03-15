# -*- coding: utf8 -*-

"Filter-related models"

from uuid import uuid4
from django.db import models

class Filter(models.Model):
    "A filter"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    layer = models.ForeignKey('backend.Layer', related_name='filters_relation')
    name = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    weight = models.IntegerField(default=0)

    @property
    def configurations(self):
        "Iterable list of configurations for this filter"
        return self.configurations_relation.all()

    @property
    def links(self):
        "Iterable list of links from this filter"
        return self.links_origin_relation.all()

    @property
    def links_in(self):
        "Iterable list of links to this filter"
        return self.links_target_relation.all()

    def config(self, key):
        "Get a configuration uuid for a given key"
        try:
            return str(self.configurations_relation.get(key=key).value.uuid)
        except Configuration.DoesNotExist:
            return None

    def links_from(self, node):
        "Get the links from this filter"
        try:
            return self.links_origin_relation.filter(origin_node=node)
        except Link.DoesNotExist:
            return None

    def link_to(self, node):
        "Get the links to this filter"
        try:
            return self.links_target_relation.filter(target_node=node)
        except Link.DoesNotExist:
            return None

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['layer__weight', 'weight']

class Configuration(models.Model):
    "A configuration for a given filter"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    target = models.ForeignKey('backend.Filter', related_name="configurations_relation")
    key = models.CharField(max_length=255)
    value = models.ForeignKey('backend.Variable')

    def get(self):
        "Get the value of this configuration"
        return self.value.get()

    def __unicode__(self):
        return self.value

class Link(models.Model):
    "A link between nodes in a workflow"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    origin_filter = models.ForeignKey('backend.Filter', related_name="links_origin_relation")
    origin_node = models.CharField(max_length=255)
    target_filter = models.ForeignKey('backend.Filter', related_name="links_target_relation")
    target_node = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.uuid)

    class Meta:
        ordering = ['origin_node']
