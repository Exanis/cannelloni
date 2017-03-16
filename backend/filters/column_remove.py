# -*- coding: utf8 -*-

"ColumnRemove filter"

from .abstract import AbstractFilter

class ColumnRemove(AbstractFilter):
    "Remove a specific column from a flux"
    name = 'Retrait de colonne'
    description = "Retire une colonne d'un flux"

    node_in = ['origine']
    node_out = ['reste']

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
        self._flux_out['reste'] = {
            'headers': origin['headers'][:column_id] + origin['headers'][column_id + 1:],
            'rows': [
                [
                    cell for ind, cell in enumerate(row) if ind != column_id
                ] for row in origin['rows']
            ]
        }
