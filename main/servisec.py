from datetime import datetime

from main.models import Agent


def send_email():
    pass


def get_agents_for_inspection():
    time_now = datetime.now().strftime('%Y-%m-%d')
    agents = Agent.objects.filter(date_of_inspection=time_now)
    return agents
