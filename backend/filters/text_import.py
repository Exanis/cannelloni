# -*- coding: utf8 -*-

"Filter definition for text_import"

from .abstract import AbstractFilter

class TextImport(AbstractFilter):
    "Import plain text file"
    name = "Importation de fichier texte"
    description = """Importe un fichier texte comme source de donnés.
    Une seule colonne sera créée"""

    node_out = ['contenu']

    parameters = [
        {
            'name': 'Fichier',
            'key': 'file',
            'type': 'file'
        }
    ]

    def run(self):
        "Import the file"
        with open(self._param('file'), 'r') as textfile:
            lines = [[line.rstrip('\n')] for line in textfile]
        output = {
            'headers': ['lines'],
            'rows': lines
        }
        self._flux_out['contenu'] = output
