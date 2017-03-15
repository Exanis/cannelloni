# -*- coding: utf8 -*-

"Filter definition for xls_import"

import csv
from .abstract import AbstractFilter

class CsvImport(AbstractFilter):
    "Import csv files"
    name = "Importation de fichier CSV"
    description = """Importe un fichier CSV comme source de donnés.
La première ligne du fichier CSV sera considérée comme le titre des colonnes."""

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
        with open(self._param('file'), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            output = {
                'headers': None,
                'rows': []
            }
            for row in reader:
                if output['headers'] is None:
                    output['headers'] = row
                else:
                    output['rows'].append(row)
            self._flux_out['contenu'] = output
