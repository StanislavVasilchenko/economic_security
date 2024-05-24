from django.core.management import BaseCommand
from psycopg2 import IntegrityError

from private_keys import FILE_NAME
import json
from main.models import Agent


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)

        for agent in data:
            try:
                Agent.objects.create(**agent)
            except Exception as e:
                continue

        # agents = [Agent(**agent) for agent in data]
        #
        # for agent in agents:
        #     try:
        #         Agent.objects.create(agent=agent)
        #         # agent.save()
        #     except Exception as e:
        #         continue


