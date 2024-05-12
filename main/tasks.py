from datetime import datetime

from celery import shared_task

from main.models import Agent, ReportStatus
from main.servisec import send_email_to_agent


@shared_task
def get_agents_for_inspection():
    time_now = datetime.now().strftime('%Y-%m-%d')
    agents = Agent.objects.filter(date_of_inspection=time_now)
    if agents.count() > 0:
        for agent in agents:
            send_email_to_agent(agent)

            agent.report_status = ReportStatus.UNDER_INSPECTION
            agent.departure_date = time_now
            agent.save()
