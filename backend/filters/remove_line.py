# -*- coding: utf8 -*-

"Filter definition for remove_line"

from copy import copy
from .abstract import AbstractFilter

class RemoveLine(AbstractFilter):
    "Remove a line from result"
    name = "Retrait de ligne"
    description = """Retire une ligne donnée d'un flux"""

    node_in = ['origine']
    node_out = ['resultat']

    parameters = [
        {
            'name': 'Ligne cible',
            'key': 'target',
            'type': 'integer'
        }
    ]

    def run(self):
        "Remove the line"
        flux = self._flux_in['origine']
        target = self._param('target')
        if target < 0:
            target = len(flux['rows']) + target
        output = {
            'headers': copy(flux['headers']),
            'rows': flux['rows'][:target] + flux['rows'][target + 1:]
        }
        self._flux_out['resultat'] = output
