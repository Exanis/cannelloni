# -*- coding: utf8 -*-

"Uppercase filter"

from copy import copy
from .abstract import AbstractFilter

class UppercaseAll(AbstractFilter):
    "Switch all fields to uppercase"
    name = 'Tous majuscule'
    description = "Passe le contenu de toutes les colonnes"

    node_in = ['contenu']
    node_out = ['resultat']

    parameters = []

    def run(self):
        "Execute the filter"
        origin = self._flux_in['contenu']
        self._flux_out['resultat'] = {
            'headers': copy(origin['headers']),
            'rows': [
                [
                    value.upper() for value in row
                ] for row in origin['rows']
            ]
        }
