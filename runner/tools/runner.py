# -*- coding: utf8 -*-

"Runner class to run a workflow"

import os
import traceback
import sys
from json import dump as json_dump
from uuid import uuid4
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
        self._logfile = os.path.join("runner", "status", "%s.log" % workflow_uuid)
        self._step = step
        self._pid = os.getpid()
        self._watch = watch
        self._commands_file = os.path.join("runner", "status", "%s.%s" % (
            str(self._workflow.uuid),
            self._watch,
        ))

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
        if self._step:
            print str(target['model'].uuid)
            sys.stdout.flush()
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
            sys.stdout.flush()
            return False

    def _dump(self):
        dump = {
            "variables": self._registery.dump_variables(),
            "filters": [{
                "name": fil['model'].name,
                "dump": fil['klass'].dump()
            } for fil in self._ordered_filters],
            "misc": {
                "status": self._registery.is_done()
            }
        }
        target = uuid4()
        dump_target = os.path.join("runner", "status", "%s.dump" % str(target))
        with open(dump_target, 'w+') as dump_target:
            json_dump(dump, dump_target)
        print "dump %s" % str(target)
        sys.stdout.flush()

    # Note: we are not using a pipe here as subprocess.Popen seems
    # to bug when stdin and stdout are filed on python 2.7 on windows
    def _read_a_line(self):
        with open(self._commands_file, 'r') as command:
            return command.readline()

    def _consume_command(self):
        with open(self._commands_file, 'w') as _:
            pass

    def _wait_step(self):
        if self._step:
            line = self._read_a_line()
            while line not in ["step", "run", "quit"]:
                if line == "dump":
                    self._dump()
                    self._consume_command()
                line = self._read_a_line()
            if line == "run":
                self._step = False
            elif line == "quit":
                quit()
            self._consume_command()

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
