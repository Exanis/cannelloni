# -*- coding: utf8 -*-

"Filter definition for keep_line"

from copy import copy
from .abstract import AbstractFilter

class KeepLine(AbstractFilter):
    "Keep only a line from result"
    name = "Sélection de ligne"
    description = """Ne garde qu'une seule ligne d'un flux"""

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
        "Select the line"
        flux = self._flux_in['origine']
        target = self._param('target')
        output = {
            'headers': copy(flux['headers']),
            'rows': [copy(flux['rows'][target]) if target < len(flux['rows']) else []]
        }
        self._flux_out['resultat'] = output
