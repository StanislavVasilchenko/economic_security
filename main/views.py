from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView

from main.forms import AgentForm
from main.models import Agent, ReportStatus
from main.servisec import context_data_index, agents_for_inspection, agents_under_inspection, agents_expired_inspection
from main.tasks import get_agents_for_inspection, send_mail_to_agent


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


class AgentDetailView(DetailView):
    model = Agent


class AgentUpdateView(UpdateView):
    model = Agent
    form_class = AgentForm
    success_url = reverse_lazy('main:index')


class AgentForInspectionView(TemplateView):
    """Выбор КА для проверки"""
    template_name = 'main/agents_for_inspections.html'
    model = Agent

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = agents_for_inspection()
        return context_data


class AgentCreateView(CreateView):
    model = Agent
    form_class = AgentForm
    success_url = reverse_lazy('main:agents-list')


class AgentPendingConfirmationView(TemplateView):
    model = Agent
    template_name = 'main/agents_pending_confirmation.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = agents_under_inspection()
        return context_data


class AgentWithExpired(TemplateView):
    model = Agent
    template_name = 'main/agents_with_expired_date.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = agents_expired_inspection()
        return context_data


def send_agents_report(request):
    """Кнопка для ручной отправки писем """
    if request.method == 'POST':
        get_agents_for_inspection.delay()
        return HttpResponseRedirect(reverse_lazy('main:index'))


def send_email_agents_ex(request):
    """Кнопка для отправки писем всем агентам с просроченой датой проверки"""
    if request.method == 'POST':
        agents_report = Agent.objects.filter(date_of_inspection__lt=datetime.now(),
                                             report_status__in=[ReportStatus.VERIFIED, ReportStatus.NOT_VERIFIED],
                                             email__isnull=False)
        send_mail_to_agent(agents_report)
        # send_email_to_agent_expired.delay()
        return HttpResponseRedirect(reverse_lazy('main:index'))
