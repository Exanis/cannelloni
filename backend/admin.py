# -*- coding: utf8 -*-

"Admin definitions"

from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from backend import models

class TypeAdmin(admin.ModelAdmin):
    "Type administration class"
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.Namespace, GuardedModelAdmin)
admin.site.register(models.Type, TypeAdmin)
