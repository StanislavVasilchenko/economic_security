from datetime import datetime, timedelta

from django.contrib import admin

from main.models import Agent, FileReport, ReportStatus


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inn',
                    'date_of_inspection', 'counterparty_form',
                    'report_status', 'is_active')
    search_fields = ('name', 'email', 'inn')
    list_editable = ('date_of_inspection', 'report_status',)
    list_filter = ('report_status', 'counterparty_form', 'date_of_inspection', 'is_active')
    actions = ['change_status', 'change_date', 'change_date_of_inspection', 'change_status_and_date',]
    ordering = ('date_of_inspection',)

    def change_status(self, request, queryset):
        queryset.update(report_status=ReportStatus.VERIFIED)

    change_status.short_description = 'Изменить статус на проверен'

    def change_date(self, request, queryset):
        queryset.update(date_of_inspection=datetime.strptime('2020-01-01', '%Y-%m-%d'))

    change_date.short_description = 'Заменить пустую дату'

    def change_date_of_inspection(self, request, queryset):
        next_inspection = datetime.now().date() + timedelta(weeks=52)
        queryset.update(date_of_inspection=next_inspection)

    change_date_of_inspection.short_description = (f"Изменить дату проверки на"
                                                   f" {datetime.now().date() + timedelta(weeks=52)}")

    def change_status_and_date(self, request, queryset):
        queryset.update(report_status=ReportStatus.VERIFIED,
                        date_of_inspection=datetime.now().date() + timedelta(weeks=52))

    change_status_and_date.short_description = (f'Изменить статус и дату проверки'
                                                f' {datetime.now().date() + timedelta(weeks=52)}')


@admin.register(FileReport)
class FileReportAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'file_name', 'date_created',
                    'agent')
