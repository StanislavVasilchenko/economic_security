from datetime import datetime, timedelta

from celery.worker.consumer import agent
from django.core.mail import EmailMessage

from main.models import Agent, ReportStatus
from app_config.settings import EMAIL_HOST_USER
from private_keys import URL_UL, URL_FL


def send_email_to_agent(agent: Agent):
    """Отправка почты КА с копией отправителю"""
    email = EmailMessage(
        subject=f'Опросник КА {agent.name} ИНН {agent.inn}, договор размещения оборудования ООО "Сеть"',
        body=f'Сылка на опросник : {URL_UL}'
        if agent.counterparty_form == 'Юридическое лицо' else f'Сылка на опросник :{URL_FL}',

        from_email=EMAIL_HOST_USER,
        to=[agent.email],
        bcc=[EMAIL_HOST_USER]
    )
    email.send()


def change_after_send_email(agent: Agent):
    """Изменение статуса КА и даты проверки"""
    time_now = datetime.now().strftime('%Y-%m-%d')
    agent.report_status = ReportStatus.UNDER_INSPECTION
    agent.departure_date = time_now

    agent.save()


def context_data_index():
    date_inspection = datetime.now().date() + timedelta(days=7)
    context_data = {
        'agents_count': Agent.objects.filter(date_of_inspection=date_inspection,
                                             email__isnull=False,
                                             report_status=ReportStatus.NOT_VERIFIED).count()
    }
    return context_data
