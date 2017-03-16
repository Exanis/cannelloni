# -*- coding: utf8 -*-

"Concat filter"

from .abstract import AbstractFilter

class Concat(AbstractFilter):
    "Concat two variables"
    name = 'Concaténer variables'
    description = "Concatène deux variables dans une troisième"

    parameters = [
        {
            'name': 'Variable 1',
            'key': 'target1',
            'type': 'string'
        },
        {
            'name': 'Variable 2',
            'key': 'target2',
            'type': 'string'
        },
        {
            'name': 'Cible',
            'key': 'dest',
            'type': 'string'
        }
    ]

    def run(self):
        "Execute the filter"
        target1 = self._param('target1')
        target2 = self._param('target2')
        dest = self._model.config('dest')
        self._registery.set(dest, "%s%s" % (target1, target2,))
