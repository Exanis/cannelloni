# -*- coding: utf8 -*-

"Registery class used to manage variables on the workflow"

from backend import models

class Registery(object):
    "Simple tool to manage variables"

    _variables = {}

    def __init__(self, namespace):
        variables = models.Variable.objects.filter(group__namespace__uuid=namespace)
        for variable in variables:
            self._variables[str(variable.uuid)] = variable.get()

    def get(self, variable):
        "Get the value of a variable"
        return self._variables[variable]

    def set(self, variable, value):
        "Set the value of a variable"
        self._variables[variable] = value
