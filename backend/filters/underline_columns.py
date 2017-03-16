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
            'rows': []
        }
        tmp = [[]]
        longest = 0
        for line in lines:
            if len(line) > 0 and all(letter in underline for letter in line):
                output['headers'].append(prev)
                tmp.append([])
                current = current + 1
                prev = None
            else:
                if prev is not None:
                    tmp[current].append(prev)
                if len(tmp[current]) > longest:
                    longest = len(tmp[current])
                prev = line
        if prev is not None:
            tmp[current].append(prev)
        output['rows'] = [
            [
                col[row] if row < len(col) else '' for col in tmp
            ] for row in range(longest)
        ]
        self._flux_out['resultat'] = output
