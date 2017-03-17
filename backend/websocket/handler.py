# -*- coding: utf8 -*-

"Websocket handler class"

import os
import subprocess
from time import sleep
from uuid import uuid4
from threading import Thread
from channels.generic.websockets import JsonWebsocketConsumer
from cannelloni import settings

class Handler(JsonWebsocketConsumer):
    "Handler for websocket commands"

    _handlers = {}

    def _update_status(self, flux, watch):
        print "start"
        for line in iter(flux.readline, b''):
            print "======%s" % line
            if line == "Error":
                self.send({'command': 'status', "status": "Error"})
            else:
                self.send({'command': 'status', "status": "Running", "filter": line})
        self.send({'command': 'status', "status": "Done"})
        self._handlers[watch].close()

    def _say(self, uuid, command):
        self._handlers[uuid].write("%s\n" % command)

    def _play(self, params, step):
        workflow_id = params['uuid']
        watch = str(uuid4())
        runner = "run.bat" if os.name == "nt" else "run.sh"
        params = [
            os.path.join(settings.BASE_DIR, runner),
            workflow_id,
            watch
        ]
        if step:
            params.append("--step")
        process = subprocess.Popen(params, stdout=subprocess.PIPE, bufsize=1)
        print "%s.%s" % (workflow_id, watch,)
        file_handler = open(os.path.join(
            settings.BASE_DIR,
            "runner",
            "status",
            "%s--.%d" % (workflow_id, process.pid,)), "w+")
        self._handlers[watch] = file_handler
        thread = Thread(target=self._update_status, args=(process.stdout, watch,))
        thread.daemon = True
        thread.start()
        self.send({'command': 'started', 'id': watch})

    def _step(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._say(process_id, "step")

    def _run(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._say(process_id, "run")

    def _quit(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._say(process_id, "quit")

    def _dump(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._say(process_id, "dump")
            sleep(0.1)
            pass

    def receive(self, content):
        "Handle the command"
        if content['command'] == u"play":
            self._play(content, False)
        elif content['command'] == u"start":
            self._play(content, True)
        elif content['command'] == u"step":
            self._step(content)
        elif content['command'] == u"run":
            self._run(content)
        elif content['command'] == u"quit":
            self._quit(content)
        elif content['command'] == u"dump":
            self._dump(content)
