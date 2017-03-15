# -*- coding: utf8 -*-

"Export a flux to a csv file"

from .abstract import AbstractFilter

class CsvExport(AbstractFilter):
    "Export a flux to a csv file"
    name = "Exportateur CSV"
    description = "Export un fichier en CSV"

    node_in = ['contenu']

    parameters = [
        {
            'name': 'Chemin d\'enregistrement',
            'key': 'file',
            'type': 'string'
        }
    ]

    def run(self):
        "Save the flux"
        flux = self._flux_in['contenu']
        with open(self._param('file'), 'wb+') as destination:
            destination.write(';'.join(flux['headers']))
            destination.write("\n")
            destination.write("\n".join([
                ';'.join(row) for row in flux['rows']
            ]))
            destination.write("\n")
