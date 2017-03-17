# -*- coding: utf8 -*-

"Runner class to run a workflow"

import os
import traceback
from time import sleep
from django.utils import timezone
from backend import models, filters
from .registery import Registery

class Runner(object):
    "Run a workflow"

    _step = False
    _workflow = None
    _registery = None
    _commands_file = None
    _logfile = ''
    _pid = 0

    _filters = {}
    _ordered_filters = []

    def __init__(self, workflow_uuid, watch, step):
        self._workflow = models.Workflow.objects.get(uuid=workflow_uuid)
        self._registery = Registery(self._workflow.namespace.uuid)
        self._logfile = "runner/status/%s.log" % workflow_uuid
        self._step = step
        self._pid = os.getpid()
        self._watch = watch

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
        print str(target['model'].uuid)
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
            print "Error"
            return False

    # TODO
    def _dump(self):
        pass

    def _wait_step(self):
        if self._step:
            line = self._commands_file.readline()
            while line not in ["step\n", "run\n", "quit\n"]:
                if line == "dump\n":
                    self._dump()
                line = self._commands_file.readline()
            if line == "run\n":
                self._step = False
            elif line == "quit\n":
                quit()

    def run(self):
        "Run the workflow"
        sleep(0.1)
        if self._step:
            self._commands_file = open("runner/status/%s.%s" % (
                str(self._workflow.uuid),
                self._watch,
            ), "r")
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
        if self._commands_file is not None:
            self._commands_file.close()