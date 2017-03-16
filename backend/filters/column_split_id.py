# -*- coding: utf8 -*-

"ColumnSplitId filter"

from .abstract import AbstractFilter

class ColumnSplitId(AbstractFilter):
    "Split a specific column from a flux"
    name = 'Colonne split (id)'
    description = "Retire une colonne d'un flux et créé un nouveau flux avec elle"

    node_in = ['origine']
    node_out = ['colonne', 'reste']

    parameters = [
        {
            'name': 'Colonne',
            'key': 'column',
            'type': 'integer'
        }
    ]

    def run(self):
        "Execute the filter"
        origin = self._flux_in['origine']
        column_id = self._param('column')
        self._flux_out['colonne'] = {
            'headers': [origin['headers'][column_id]],
            'rows': [[row[column_id]] for row in origin['rows'] if column_id in row]
        }
        self._flux_out['reste'] = {
            'headers': origin['headers'][:column_id] + origin['headers'][column_id + 1:],
            'rows': [
                [
                    cell for ind, cell in enumerate(row) if ind != column_id
                ] for row in origin['rows']
            ]
        }
