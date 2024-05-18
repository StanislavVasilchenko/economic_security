from datetime import datetime

from django.core.mail import send_mail

from main.models import Agent, ReportStatus
from app_config.settings import EMAIL_HOST_USER
from private_keys import URL_UL, URL_FL


def send_email_to_agent(agent: Agent):
    """Отправка почты КА"""
    send_mail(
        subject=f'Опросник КА {agent.name} ИНН {agent.inn}, договор размещения оборудования ООО "Сеть"',
        from_email=EMAIL_HOST_USER,
        message=f'Сылка на опросник : {URL_UL}'
        if agent.counterparty_form == 'Юридическое лицо' else f'Сылка на опросник :{URL_FL}',
        recipient_list=[agent.email],
    )


def change_after_send_email(agent: Agent):
    """Изменение КА после отправки письма"""
    time_now = datetime.now().strftime('%Y-%m-%d')
    agent.report_status = ReportStatus.UNDER_INSPECTION
    agent.departure_date = time_now

    agent.save()
