# -*- coding: utf8 -*-

"CountColumn filter"

from .abstract import AbstractFilter

class CountColumn(AbstractFilter):
    "Count a flux's column and put the result in a variable"
    name = 'Compter colonnes'
    description = "Compte le nombre de colonnes d'un flux et met le résultat dans une variable"

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
        value = len(self._flux_in['cible']['headers'])
        self._registery.set(target, value)
