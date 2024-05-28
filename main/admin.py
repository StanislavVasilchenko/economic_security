from datetime import datetime

from django.contrib import admin

from main.models import Agent, FileReport, ReportStatus


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'inn',
                    'departure_date', 'date_of_inspection', 'counterparty_form',
                    'report_status', 'is_active')
    search_fields = ('name', 'email', 'inn')
    list_filter = ('report_status', 'counterparty_form', 'date_of_inspection', 'is_active')
    actions = ['change_status', 'change_date', 'change_date_of_inspection', ]
    ordering = ('date_of_inspection',)

    def change_status(self, request, queryset):
        queryset.update(report_status=ReportStatus.VERIFIED)

    change_status.short_description = 'Изменить статус на проверен'

    def change_date(self, request, queryset):
        queryset.update(date_of_inspection=datetime.strptime('2020-01-01', '%Y-%m-%d'))

    change_date.short_description = 'Заменить пустую дату'

    def change_date_of_inspection(self, request, queryset):
        now = datetime.now().date()
        queryset.update(date_of_inspection=now)

    change_date_of_inspection.short_description = f"Изменить дату проверки на {datetime.now().date()}"


@admin.register(FileReport)
class FileReportAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'file_name', 'date_created',
                    'agent')
