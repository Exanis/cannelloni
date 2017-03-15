# -*- coding: utf8 -*-

"Variable related models"

from uuid import uuid4
from django.db import models
from backend import types

class Type(models.Model):
    "Type of a variable"
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    container = models.BooleanField()
    convertor = models.CharField(max_length=255, default=None, blank=True, null=True)
    handler = models.CharField(max_length=255, default=None, blank=True, null=True)
    icon = models.CharField(max_length=255, default='')

    def convert(self, variable):
        "Convert a variable to its true type"
        if self.convertor is not None and len(self.convertor) > 0:
            return getattr(types, self.convertor)(variable.value)
        else:
            return variable.value

    def handle(self, request, variable):
        "Handle a modification on a variable"
        if self.handler is not None and len(self.handler) > 0:
            getattr(types, self.handler)(request, variable)
        else:
            variable.value = unicode(request.POST[str(variable.uuid)])

    def __unicode__(self):
        return self.name

class Group(models.Model):
    "Group of variables"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    namespace = models.ForeignKey('backend.Namespace', related_name='groups_relation')
    name = models.CharField(max_length=255)

    @property
    def variables(self):
        "Iterable list of variables in this group"
        return self.variables_relation.all()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Variable(models.Model):
    "A variable model"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    group = models.ForeignKey('backend.Group', related_name='variables_relation')
    type_class = models.ForeignKey("backend.Type")
    parent = models.ForeignKey("backend.Variable", null=True, blank=True, default=None)
    name = models.CharField(max_length=255)
    value = models.TextField(default='')

    @property
    def type_slug(self):
        return self.type_class.slug

    def set(self, request):
        "Set the value of this variable"
        self.type_class.handle(request, self)
        self.save()

    def get(self):
        "Get the value of this variable as its true type"
        return self.type_class.convert(self)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
