# -*- coding: utf8 -*-

"ColumnSplit filter"

from .abstract import AbstractFilter

class ColumnSplit(AbstractFilter):
    "Split a specific column from a flux"
    name = 'Colonne split'
    description = "Retire une colonne d'un flux et créé un nouveau flux avec elle"

    node_in = ['origine']
    node_out = ['colonne', 'reste']

    parameters = [
        {
            'name': 'Colonne',
            'key': 'column',
            'type': 'string'
        }
    ]

    def run(self):
        "Execute the filter"
        origin = self._flux_in['origine']
        column = self._param('column')
        column_id = origin['headers'].index(column)
        self._flux_out['colonne'] = {
            'headers': [column],
            'rows': [[row[column_id]] for row in origin['rows'] if column_id < len(row)]
        }
        self._flux_out['reste'] = {
            'headers': origin['headers'][:column_id] + origin['headers'][column_id + 1:],
            'rows': [
                [
                    cell for ind, cell in enumerate(row) if ind != column_id
                ] for row in origin['rows']
            ]
        }
