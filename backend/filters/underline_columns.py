# -*- coding: utf8 -*-

"Filter definition for underline_columns"

from .abstract import AbstractFilter

class UnderlineColumns(AbstractFilter):
    "Create columns from underlined text file"
    name = "Colonne par souligné"
    description = """Recherche des colonnes soulignées dans un fichier texte"""

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
            'name': 'Caractères de soulignage',
            'key': 'underline',
            'type': 'string'
        }
    ]

    def run(self):
        "Find columns"
        flux = self._flux_in['fichier']
        target = self._param('target')
        header = self._param('default')
        underline = self._param('underline')
        current = 0
        prev = None
        column = flux['headers'].index(target)
        lines = [line[column] for line in flux['rows']]
        output = {
            'headers': [header],
            'rows': [[]]
        }
        for line in lines:
            if all(letter in underline for letter in line):
                output['headers'].append(prev)
                output['rows'].append([])
                current = current + 1
                prev = None
            else:
                if prev is not None:
                    output['rows'][current].append(prev)
                prev = line
        if prev is not None:
            output['rows'][current].append(prev)
        self._flux_out['resultat'] = output
