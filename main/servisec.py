from django.core.mail import send_mail

from main.models import Agent
from app_config.settings import EMAIL_HOST_USER


def send_email_to_agent(agent: Agent):
    send_mail(
        subject=f'Опросник КА {agent.name} ИНН {agent.inn}, договор размещения оборудования ООО "Сеть"',
        from_email=EMAIL_HOST_USER,
        message=f'Опросник + ссылка',
        recipient_list=[agent.email],
    )


