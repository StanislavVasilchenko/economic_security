from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from main.models import Agent, ReportStatus
from main.servisec import context_data_index
from main.tasks import get_agents_for_inspection


class HomeView(TemplateView):
    template_name = 'main/index.html'
    model = Agent

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(context_data_index())
        return context_data


class AgentListView(ListView):
    model = Agent

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Agent.objects.all().order_by('date_of_inspection')[:10]
        return context_data


class AgentForInspectionView(TemplateView):
    """Выбор КА для проверки"""
    template_name = 'main/agents_for_inspections.html'
    model = Agent

    def get_context_data(self, **kwargs):
        date_inspection = datetime.now().date() + timedelta(days=7)
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Agent.objects.filter(date_of_inspection=date_inspection,
                                                           email__isnull=False,
                                                           report_status=ReportStatus.NOT_VERIFIED)
        return context_data


class AgentCreateView(CreateView):
    model = Agent
    fields = '__all__'
    success_url = reverse_lazy('main:agents-list')


def send_agent_report(request):
    """Ручная отправка писем """
    if request.method == 'POST':
        get_agents_for_inspection()
        return render(request, 'main/agents_for_inspections.html')
