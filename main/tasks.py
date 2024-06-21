from datetime import datetime, timedelta

from celery import shared_task
from django.core.management import call_command
from django.db.models import QuerySet

from main.models import Agent, ReportStatus
from main.servisec import (send_email_to_agent, change_after_send_email,
                           agents_for_inspection)


def send_mail_to_agent(agents: QuerySet[Agent]):
    """Принимает список агентов которым необходимо разослатьписьма"""
    if agents.count() > 0:
        for agent in agents:
            print(agent.email)
            send_email_to_agent(agent)
            change_after_send_email(agent)


@shared_task
def get_agents_for_inspection():
    """Задача по выбору КА дата проверки которых совпадает с текущей датой и """
    agents = agents_for_inspection()
    send_mail_to_agent(agents)


@shared_task
def check_date_of_inspection():
    date_inspection = datetime.now().date() + timedelta(days=7)
    agents = Agent.objects.filter(date_of_inspection=date_inspection)
    if agents.count() > 0:
        for agent in agents:
            agent.report_status = ReportStatus.NOT_VERIFIED
            agent.save()


@shared_task
def create_fixture_agents():
    call_command("dumpdata", "main.agent", output="agents.json")
