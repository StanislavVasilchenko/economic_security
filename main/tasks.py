from datetime import datetime

from celery import shared_task

from main.models import Agent, ReportStatus
from main.servisec import send_email_to_agent, change_after_send_email


@shared_task
def get_agents_for_inspection():
    """Задаса по выбору КА дата проверки которых совпадает с текущей датой и """
    time_now = datetime.now().strftime('%Y-%m-%d')
    agents = Agent.objects.filter(date_of_inspection=time_now,
                                  email__isnull=False,
                                  report_status=ReportStatus.NOT_VERIFIED)
    if agents.count() > 0:
        for agent in agents:
            send_email_to_agent(agent)

            change_after_send_email(agent)
