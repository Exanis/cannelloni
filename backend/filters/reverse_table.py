# -*- coding: utf8 -*-

"Filter definition for ReverseTable"

from .abstract import AbstractFilter

class ReverseTable(AbstractFilter):
    "Reverse a table"
    name = "Renversement"
    description = """Renverse une table (les têtes de ligne deviennent tête de colonne)"""

    node_in = ['origine']
    node_out = ['resultat']

    parameters = []

    def run(self):
        "Reverse the table"
        flux = self._flux_in['origine']
        output = {
            'headers': [flux['header'][0]] + [line[0] for line in flux['rows']],
            'rows': [flux['header'][1:]] + [line[1:] for line in flux['rows']]
        }
        self._flux_out['resultat'] = output
