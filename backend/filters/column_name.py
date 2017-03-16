# -*- coding: utf8 -*-

"ColumnName filter"

from .abstract import AbstractFilter

class ColumnName(AbstractFilter):
    "Get the name of a column into a string"
    name = 'Nom de colonne'
    description = "Met le nom d'une colonne dans une variable"

    node_in = ['cible']

    parameters = [
        {
            'name': 'Colonne',
            'key': 'column',
            'type': 'integer'
        },
        {
            'name': 'Cible',
            'key': 'target',
            'type': 'string'
        }
    ]

    def run(self):
        "Execute the filter"
        column = self._param('column')
        target = self._model.config('target')
        column_name = self._flux_in['cible']['headers'][column]
        self._registery.set(target, column_name)
