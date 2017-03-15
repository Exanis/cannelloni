# -*- coding: utf8 -*-

"Namespace-related models"

from uuid import uuid4
from django.db import models

class Namespace(models.Model):
    "Namespace model"
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)

    @property
    def groups(self):
        "Iterable list of all variables groups in this namespace"
        return self.groups_relation.all()

    @property
    def workflows(self):
        "Iterable list of all workflows in this namespace"
        return self.workflows_relation.all()

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_namespace', 'Voir le namespace'),
        )
        ordering = ['name']
