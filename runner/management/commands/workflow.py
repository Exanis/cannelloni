# -*- coding: utf8 -*-

"Management command"

from django.core.management.base import BaseCommand
from runner.tools import Runner

class Command(BaseCommand):
    "Run a workflow"
    help = "Run a workflow"

    def add_arguments(self, parser):
        parser.add_argument('uuid', nargs=1)
        parser.add_argument('watcher', nargs=1)

    def handle(self, *args, **options):
        runner = Runner(options['uuid'][0], options['watcher'][0])
        runner.run()
