# -*- coding: utf8 -*-

"Websocket handler class"

import os
import subprocess
import json
import re
from time import sleep
from uuid import uuid4
from threading import Thread
from channels.generic.websockets import JsonWebsocketConsumer
from cannelloni import settings

class Handler(JsonWebsocketConsumer):
    "Handler for websocket commands"

    _handlers = {}

    def _read_dump(self, target):
        dump_file = os.path.join(
            settings.BASE_DIR,
            "runner",
            "status",
            "%s.dump" % target
        )
        with open(dump_file, "r") as dump_fp:
            dump_string = dump_fp.read()
        self.send({
            'command': 'dump',
            'dump': json.loads(dump_string)
        })
        os.remove(dump_file)

    def _update_status(self, flux, watch):
        for line in iter(flux.readline, b''):
            line = line.strip()
            if line == "Error\n":
                self.send({'command': 'status', "status": "Error"})
            else:
                search = re.search(r'^dump ([a-z0-9\-]+)', line)
                if search is not None:
                    self._read_dump(search.group(1))
                else:
                    self.send({'command': 'status', "status": "Running", "filter": line})
        self.send({'command': 'status', "status": "Done"})
        if self._handlers[watch] != '':
            os.remove(self._handlers[watch])
        self._handlers.pop(watch)

    def _say(self, uuid, command):
        with open(self._handlers[uuid], 'w') as target:
            target.write(command)

    def _play(self, params, step):
        workflow_id = params['uuid']
        watch = str(uuid4())
        runner = "run.bat" if os.name == "nt" else "run.sh"
        params = [
            os.path.join(settings.BASE_DIR, runner),
            workflow_id,
            watch
        ]
        command_file_path = os.path.join(
            settings.BASE_DIR,
            "runner",
            "status",
            "%s.%s" % (workflow_id, watch,))
        if step:
            params.append("--step")
            with open(command_file_path, 'w+') as _: # Just create file
                pass
            self._handlers[watch] = command_file_path
        else:
            self._handlers[watch] = ''
        process = subprocess.Popen(params, stdout=subprocess.PIPE, bufsize=1)
        thread = Thread(target=self._update_status, args=(process.stdout, watch))
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
