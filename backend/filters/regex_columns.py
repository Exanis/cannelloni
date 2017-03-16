# -*- coding: utf8 -*-

"Filter definition for regex_columns"

import re
from .abstract import AbstractFilter

class RegexColumns(AbstractFilter):
    "Create columns from a regex"
    name = "Colonne par expression régulière"
    description = """Recherche des colonnes par comparaison à une expression régulière"""

    node_in = ['fichier']
    node_out = ['resultat']

    parameters = [
        {
            'name': 'Colonne cible',
            'key': 'target',
            'type': 'string'
        },
        {
            'name': 'Colonne par défaut',
            'key': 'default',
            'type': 'string'
        },
        {
            'name': 'Expression régulière',
            'key': 'regex',
            'type': 'string'
        }
    ]

    def run(self):
        "Find columns"
        flux = self._flux_in['fichier']
        target = self._param('target')
        header = self._param('default')
        regex = self._param('regex')
        current = 0
        column = flux['headers'].index(target)
        lines = [line[column] for line in flux['rows']]
        output = {
            'headers': [header],
            'rows': [[]]
        }
        for line in lines:
            match = re.search(regex, line)
            if match is not None:
                output['headers'].append(match.group(1))
                output['rows'].append([])
                current = current + 1
            else:
                output['rows'][current].append(line)
        self._flux_out['resultat'] = output
