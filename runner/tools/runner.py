# -*- coding: utf8 -*-

"Runner class to run a workflow"

import os
import traceback
import sys
from django.utils import timezone
from backend import models, filters
from cannelloni import settings
from .registery import Registery

class Runner(object):
    "Run a workflow"

    _workflow = None
    _registery = None
    _watchfile = ''
    _logfile = ''

    _filters = {}
    _ordered_filters = []

    def __init__(self, workflow_uuid, watchfile):
        self._workflow = models.Workflow.objects.get(uuid=workflow_uuid)
        self._registery = Registery(self._workflow.namespace.uuid)
        self._watchfile = os.path.join(settings.STATUS_FILES, watchfile)
        self._logfile = "%s.log" % self._watchfile

    def _load_filters(self):
        filters_list = models.Filter.objects.filter(layer__workflow=self._workflow)
        for fil in filters_list:
            self._filters[fil.uuid] = {
                'model': fil,
                'klass': getattr(filters, fil.target)(fil.uuid, self._registery)
            }
            self._ordered_filters.append(self._filters[fil.uuid])

    def _log(self, what, short=None):
        if short is not None:
            with open(self._watchfile, "w+") as pointer:
                pointer.write(str(short))
        with open(self._logfile, "a+") as pointer:
            log = u"[%s] %s\n" % (timezone.now(), unicode(what),)
            pointer.write(log)

    def _run_filter(self, target):
        self._log(
            "Starting working on filter %s (UUID %s)" % (
                target['model'].name,
                target['model'].uuid,
            ),
            target['model'].uuid
        )
        for flux in target['model'].links_in:
            target['klass'].input(
                flux.target_node,
                self._filters[flux.origin_filter.uuid]['klass'].output(flux.origin_node)
            )
        try:
            target['klass'].run()
            return True
        except:
            self._log(
                "An error occured: %s" % traceback.format_exc(),
                "Error"
            )
            return False

    def run(self):
        "Run the workflow"
        self._log("Starting workflow execution", "Starting")
        self._load_filters()
        self._log("Filters loaded")
        while self._registery.is_done() is False:
            self._registery.done()
            for fil in self._ordered_filters:
                if not self._run_filter(fil):
                    return
        self._log("Workflow execution ended", "Done")
