# -*- coding: utf8 -*-

"Filter definition for empty_lines"

from copy import copy
from .abstract import AbstractFilter

class EmptyLines(AbstractFilter):
    "Remove empty lines from result"
    name = "Retrait des lignes vides"
    description = """Retire toutes les lignes vides d'un flux"""

    node_in = ['origine']
    node_out = ['resultat']

    def run(self):
        "Remove the line"
        flux = self._flux_in['origine']
        output = {
            'headers': copy(flux['headers']),
            'rows': [row for row in flux['rows'] if any(cell is not '' for cell in row)]
        }
        self._flux_out['resultat'] = output
