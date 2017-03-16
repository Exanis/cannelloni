# -*- coding: utf8 -*-

"Strip filter"

from copy import copy
from .abstract import AbstractFilter

class Strip(AbstractFilter):
    "Strip blank from start and end of a column"
    name = 'Strip'
    description = "Retire les espaces en début et fin de colonne"

    node_in = ['contenu']
    node_out = ['resultat']

    parameters = [
        {
            'name': 'Colonne',
            'key': 'column',
            'type': 'string'
        }
    ]

    def run(self):
        "Execute the filter"
        origin = self._flux_in['contenu']
        column = self._param('column')
        column_id = origin['headers'].index(column)
        self._flux_out['resultat'] = {
            'headers': copy(origin['headers']),
            'rows': [
                [
                    value if ind != column_id else value.strip() for ind, value in enumerate(row)
                ] for row in origin['rows']
            ]
        }
