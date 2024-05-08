from django.contrib import admin

from main.models import Agent, FileReport


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'inn',
                    'departure_date', 'date_of_inspection', 'counterparty_form',
                    'report_status', 'is_active')


@admin.register(FileReport)
class FileReportAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'file_name', 'date_created',
                    'agent')
