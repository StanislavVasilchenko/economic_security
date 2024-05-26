from datetime import datetime, timedelta
from typing import List

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
    """Данные для индексной страницы
    agents_count - Кол-во Агентов которые должны быть проверены в ближайшие 7 дней
    agents_under_inspection - Кол-во Агентов которым отправлены опросники
    verification_period_expired - Кол-во Агентов с просроченной датой проверки"""
    date_inspection = datetime.now().date() + timedelta(days=7)

    context_data = {
        'agents_count': agents_for_inspection().count(),
        'agents_under_inspection': agents_under_inspection().count(),
        'verification_period_expired': Agent.objects.filter(date_of_inspection__lt=date_inspection).count()
    }
    return context_data


def agents_for_inspection() -> List[Agent]:
    """Выбор агентов для проверки которые были ранее провернены и у которых приблежается очередная
    дата проверки"""
    date_inspection = datetime.now()
    agents = Agent.objects.filter(date_of_inspection__gte=date_inspection,
                                  date_of_inspection__lte=date_inspection + timedelta(days=7),
                                  email__isnull=False,
                                  report_status=ReportStatus.VERIFIED)
    return agents


def agents_under_inspection() -> List[Agent]:
    """Выбор агентов которым отправлены письма и находящихся на проверке"""
    agents = Agent.objects.filter(report_status=ReportStatus.UNDER_INSPECTION)
    return agents


def agents_without_inspection() -> List[Agent]:
    """Выбор аггентов без проверки"""
    agents = Agent.objects.filter()
    ...
