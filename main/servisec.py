from datetime import datetime, timedelta
from typing import List

from django.core.mail import EmailMessage
from django.db.models import QuerySet

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
        bcc=[EMAIL_HOST_USER, 'a.smokvin@zelenaya.net']
    )
    email.send()


def change_after_send_email(agent: Agent):
    """Изменение статуса КА и даты проверки"""
    time_now = datetime.now().strftime('%Y-%m-%d')
    agent.report_status = ReportStatus.UNDER_INSPECTION
    agent.departure_date = time_now
    agent.date_of_inspection = None

    agent.save()


def agents_without_mail():
    """Выбор агентов без эл.почты"""
    agents = Agent.objects.filter(email__isnull=True,
                                  is_active=True)
    return agents


def context_data_index():
    """Данные для индексной страницы
    agents_count - Кол-во Агентов которые должны быть проверены в ближайшие 7 дней
    agents_under_inspection - Кол-во Агентов которым отправлены опросники
    verification_period_expired - Кол-во Агентов с просроченной датой проверки
    agents_without_mail - агенты с отсутствующем адресом эл. почты"""

    context_data = {
        'agents_count': agents_for_inspection().count(),
        'agents_under_inspection': agents_under_inspection().count(),
        'verification_period_expired': agents_expired_inspection().count(),
        'agents_without_mail': agents_without_mail()
    }
    return context_data


def agents_for_inspection() -> List[Agent]:
    """Выбор агентов для проверки которые были ранее провернены и у которых приблежается очередная
    дата проверки"""
    date_inspection = datetime.now()
    agents = Agent.objects.filter(date_of_inspection__gt=date_inspection,
                                  date_of_inspection__lte=date_inspection + timedelta(days=7),
                                  email__isnull=False,
                                  report_status=ReportStatus.VERIFIED)
    return agents


def agents_under_inspection() -> QuerySet[Agent]:
    """Выбор агентов которым отправлены письма и находящихся на проверке"""
    agents = Agent.objects.filter(report_status=ReportStatus.UNDER_INSPECTION,
                                  is_active=True)
    return agents


def agents_expired_inspection() -> List[Agent]:
    """Выбор агентов с просроченной датой проверки (кроме агентов со статусом на проверке)"""
    date_inspection = datetime.now().date()
    agents = Agent.objects.filter(date_of_inspection__lt=date_inspection,
                                  report_status__in=[ReportStatus.VERIFIED, ReportStatus.NOT_VERIFIED],
                                  email__isnull=False,
                                  is_active=True)
    return agents
