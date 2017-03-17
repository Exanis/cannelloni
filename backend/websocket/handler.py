# -*- coding: utf8 -*-

"Websocket handler class"

import os
import subprocess
from json import loads
from time import sleep
from uuid import uuid4
from channels.generic.websockets import JsonWebsocketConsumer
from cannelloni import settings

class Handler(JsonWebsocketConsumer):
    "Handler for websocket commands"

    _handlers = {}

    def _say(self, uuid, command):
        self._handlers[uuid].stdin.write("%s\n" % command)

    def _listen(self, uuid):
        return self._handlers[uuid].stdout.read()

    def _play(self, params):
        workflow_id = params['uuid']
        watch = str(uuid4())
        runner = "run.bat" if os.name == "nt" else "run.sh"
        process = subprocess.Popen([
            os.path.join(settings.BASE_DIR, runner),
            workflow_id
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self._handlers[watch] = process
        self.send({'command': 'started', 'id': watch})

    def _start(self, params):
        workflow_id = params['uuid']
        watch = str(uuid4())
        runner = "run.bat" if os.name == "nt" else "run.sh"
        process = subprocess.Popen([
            os.path.join(settings.BASE_DIR, runner),
            workflow_id,
            "--step"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self._handlers[watch] = process
        self.send({'command': 'started', 'id': watch})

    def _step(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._say(process_id, "step")

    def _quit(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._say(process_id, "quit")

    def _dump(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._say(process_id, "dump")
            sleep(0.1)
            self.send({
                'command': 'dump',
                'content': loads(self._listen(process_id))
            })

    def _status(self, params):
        process_id = params['uuid']
        if process_id in self._handlers:
            self._handlers[process_id].poll()
            print "Status for %s is %s" % (process_id, self._handlers[process_id].returncode)
            if self._handlers[process_id].returncode is not None:
                self._handlers.pop(process_id)
                self.send({'command': 'status', "status": "Done"})
            else:
                message = self._listen(process_id)
                if message is None or message == '':
                    self.send({'command': 'status', "status": "Unchanged"})
                self.send({'command': 'status', "status": message})

    def receive(self, content):
        "Handle the command"
        if content['command'] == u"play":
            self._play(content)
        elif content['command'] == u"start":
            self._start(content)
        elif content['command'] == u"step":
            self._step(content)
        elif content['command'] == u"quit":
            self._quit(content)
        elif content['command'] == u"dump":
            self._dump(content)
        elif content['command'] == u"status":
            self._status(content)
