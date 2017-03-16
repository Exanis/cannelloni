# -*- coding: utf8 -*-

"Increment filter"

from .abstract import AbstractFilter

class Increment(AbstractFilter):
    "Increment a variable"
    name = 'Incrémenter variable'
    description = "Incrémente une variable numérique"

    parameters = [
        {
            'name': 'Variable',
            'key': 'target',
            'type': 'integer'
        },
        {
            'name': 'Valeur',
            'key': 'inc',
            'type': 'integer'
        }
    ]

    def run(self):
        "Execute the filter"
        inc = self._param('inc')
        target = self._model.config('target')
        target_value = self._param('target')
        self._registery.set(target, target_value + inc)
