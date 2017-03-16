# -*- coding: utf8 -*-

"Count filter"

from .abstract import AbstractFilter

class Count(AbstractFilter):
    "Count a flux and put the result in a variable"
    name = 'Compter lignes'
    description = "Compte le nombre de lignes d'un flux et met le résultat dans une variable"

    node_in = ['cible']

    parameters = [
        {
            'name': 'Variable',
            'key': 'target',
            'type': 'integer'
        }
    ]

    def run(self):
        "Execute the filter"
        target = self._model.config('target')
        value = len(self._flux_in['cible']['rows'])
        self._registery.set(target, value)
