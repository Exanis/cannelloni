# -*- coding: utf8 -*-

"Until filter"

from .abstract import AbstractFilter

class Until(AbstractFilter):
    "Keep working until two variables are equal"
    name = 'Boucle "jusqu\'à"'
    description = "Continue à executer le workflow jusqu'à ce que deux variables soient égales"

    parameters = [
        {
            'name': 'Variable 1',
            'key': 'target',
            'type': 'integer'
        },
        {
            'name': 'Variable 2',
            'key': 'comp',
            'type': 'integer'
        }
    ]

    def run(self):
        "Execute the filter"
        target = self._param('target')
        comp = self._param('comp')
        if target != comp:
            self._registery.done(False)
