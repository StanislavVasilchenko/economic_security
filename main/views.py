from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from main.models import Agent
from main.servisec import context_data_index


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
