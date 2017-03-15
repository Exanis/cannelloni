# -*- coding: utf8 -*-

"Uppercase filter"

from copy import copy
from .abstract import AbstractFilter

class Uppercase(AbstractFilter):
    "Switch a field to uppercase"
    name = 'Majuscule'
    description = "Passe le contenu d'une colonne en majuscule"

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
                    value if ind != column_id else value.upper() for ind, value in enumerate(row)
                ] for row in origin['rows']
            ]
        }
