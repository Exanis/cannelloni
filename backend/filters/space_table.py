# -*- coding: utf8 -*-

"Filter definition for SpaceTable"

from .abstract import AbstractFilter

class SpaceTable(AbstractFilter):
    "Create a flux from a space-separated table"
    name = "Flux de table espacé"
    description = """Créé un flux à partir d'une suite de ligne formant une table
    séparée par des espaces"""

    node_in = ['origine']
    node_out = ['resultat']

    parameters = []

    def run(self):
        "Find columns"
        flux = self._flux_in['origine']
        output = {
            'headers': None,
            'rows': []
        }
        for line in flux['rows']:
            if output['headers'] is None:
                output['headers'] = line[0].split()
            elif line[0] is not '':
                output['rows'].append(line[0].split())
        self._flux_out['resultat'] = output
