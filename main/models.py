from django.db import models

from users.models import NULLABLE


class ReportStatus(models.TextChoices):
    """Статус проверки контр-агента"""

    VERIFIED = "Проверен", "Проверен"
    NOT_VERIFIED = "Не проверен", "Не проверен"
    UNDER_INSPECTION = "На проверке", "На проверке"


class FileReport(models.Model):
    """Модель для файла-отчета об отпраки письма"""

    file_path = models.CharField(max_length=255, verbose_name="Путь к файлу")
    file_name = models.CharField(max_length=255, verbose_name="Имя файла")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    agent = models.ForeignKey('Agent', on_delete=models.PROTECT, verbose_name="Агент", **NULLABLE)

    def __str__(self):
        return f"{self.file_name}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"


class Agent(models.Model):
    """Модель контр-агента:
    - name: Наименование КА
    - email: Электронная почта
    - phone: Телефон
    - inn: ИНН контр-агента
    - date_of_inspection: дата проверки
    - date_next_inspection: дата следующей проверки
    - counterparty_form: форма контр-агента(ЮЛ/ФЛ)
    - file_report: pdf файл с очетом об отпраки
    - report_status: статус проверки (Не проверен / На проверке / Проверен)
    - is_active: Статус КА"""

    ENTITY = 'Юридическое лицо'
    INDIVIDUAL = 'Физическое лицо'

    FORM = [
        (ENTITY, 'Юридическое лицо'),
        (INDIVIDUAL, 'Физическое лицо'),
    ]

    ACTIVE = 'Действующий'
    DEACTIVATED = 'Не действующий'

    name = models.CharField(max_length=60, unique=True, verbose_name='контр-агент')
    email = models.EmailField(verbose_name='Электронная почта', **NULLABLE)
    phone = models.CharField(max_length=15, verbose_name='Телефон', **NULLABLE)
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    departure_date = models.DateField(verbose_name='Дата отправки письма', **NULLABLE)
    date_of_inspection = models.DateField(verbose_name='Дата проверки', **NULLABLE)
    counterparty_form = models.CharField(max_length=50, choices=FORM, verbose_name='Форма КА', default=ENTITY)
    report_status = models.CharField(max_length=50,
                                     choices=ReportStatus.choices,
                                     verbose_name='Статус проверки',
                                     default=ReportStatus.NOT_VERIFIED)
    is_active = models.BooleanField(default=True, verbose_name='Статус', choices=[(True, ACTIVE), (False, DEACTIVATED)])

    def __str__(self):
        return f'{self.name} - ({self.email} статус: {self.report_status})'

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'
        ordering = ['-date_of_inspection']
