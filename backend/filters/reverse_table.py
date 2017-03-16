# -*- coding: utf8 -*-

"Filter definition for ReverseTable"

from copy import copy
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
        headers = [flux['headers'][0]] + [line[0] for line in flux['rows']]
        rows = [
            [value] + [line[ind + 1] for line in flux['rows']]
            for ind, value in enumerate(flux['headers'][1:])
        ]
        output = {
            'headers': headers,
            'rows': rows
        }
        self._flux_out['resultat'] = output
