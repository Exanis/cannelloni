# -*- coding: utf8 -*-

"Abstract filter definition"

from backend import models

class AbstractFilter(object):
    "Abstract filter to give the default list of fields"
    name = 'Abstract filter'
    description = 'Please fill the description'

    node_in = []
    node_out = []

    parameters = []

    _flux_in = {}
    _flux_out = {}

    _model = None

    _registery = None

    def __init__(self, uuid, registery):
        self._model = models.Filter.objects.get(uuid=uuid)
        self._registery = registery

    def input(self, node, flux):
        "Set a flux as an input value"
        self._flux_in[node] = flux

    def output(self, node):
        "Get the output flux specified"
        return self._flux_out[node]

    def _param(self, key):
        "Get a specific parameter"
        return self._registery.get(self._model.config(key))

    def run(self):
        "Run the filter. This method shall be overrided"
        pass
