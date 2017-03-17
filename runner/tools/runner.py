# -*- coding: utf8 -*-

"Runner class to run a workflow"

import os
import traceback
import json
import sys
from django.utils import timezone
from backend import models, filters
from .registery import Registery

class Runner(object):
    "Run a workflow"

    _step = False
    _workflow = None
    _registery = None
    _logfile = ''
    _pid = 0

    _filters = {}
    _ordered_filters = []

    def __init__(self, workflow_uuid, step):
        self._workflow = models.Workflow.objects.get(uuid=workflow_uuid)
        self._registery = Registery(self._workflow.namespace.uuid)
        self._logfile = "runner/status/%s.log" % workflow_uuid
        self._step = step
        self._pid = os.getpid()

    def _load_filters(self):
        filters_list = models.Filter.objects.filter(layer__workflow=self._workflow)
        for fil in filters_list:
            self._filters[fil.uuid] = {
                'model': fil,
                'klass': getattr(filters, fil.target)(fil.uuid, self._registery)
            }
            self._ordered_filters.append(self._filters[fil.uuid])

    def _log(self, what):
        with open(self._logfile, "a+") as pointer:
            log = u"[%d][%s] %s\n" % (self._pid, timezone.now(), unicode(what),)
            pointer.write(log)

    def _run_filter(self, target):
        self._log(
            "Starting working on filter %s (UUID %s)" % (
                target['model'].name,
                target['model'].uuid,
            )
        )
        json.dump({
            "filter": str(target['model'].uuid)
        }, sys.stdout)
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
                "An error occured: %s" % traceback.format_exc()
            )
            json.dump({
                'error': traceback.format_exc()
            }, sys.stdout)
            return False

    # TODO
    def _dump(self):
        pass

    def _wait_step(self):
        if self._step:
            line = raw_input()
            while line not in ["step", "play", "quit"]:
                if line == "dump":
                    self._dump()
                line = raw_input()
            if line == "play":
                self._step = False
            elif line == "quit":
                quit()

    def run(self):
        "Run the workflow"
        self._log("Starting workflow execution")
        self._load_filters()
        self._log("Filters loaded")
        while not self._registery.is_done():
            self._registery.done()
            for fil in self._ordered_filters:
                if not self._run_filter(fil):
                    self._wait_step()
                    return
                self._wait_step()
        self._log("Workflow execution ended")
