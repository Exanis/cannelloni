# -*- coding: utf8 -*-

"Registery class used to manage variables on the workflow"

from backend import models

class Registery(object):
    "Simple tool to manage variables"

    _variables = {}
    _names = {}
    _done = False

    def __init__(self, namespace):
        variables = models.Variable.objects.filter(group__namespace__uuid=namespace)
        for variable in variables:
            self._variables[str(variable.uuid)] = variable.get()
            self._names[str(variable.uuid)] = variable.name

    def get(self, variable):
        "Get the value of a variable"
        return self._variables[variable]

    def set(self, variable, value):
        "Set the value of a variable"
        self._variables[variable] = value

    def done(self, value=True):
        "Set if the workflow is done or not"
        self._done = value

    def is_done(self):
        "Get the status of the workflow"
        return self._done

    def dump_variables(self):
        "Dump variables status"
        return [
            {
                "name": self._names[uuid],
                "value": self._variables[uuid]
            } for uuid in self._names
        ]
