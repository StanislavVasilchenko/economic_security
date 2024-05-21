from django.urls import path

from main.apps import MainConfig
from main.views import HomeView, AgentListView, AgentForInspectionView, send_agent_report, AgentCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('agents/', AgentListView.as_view(), name='agents-list'),
    path('inspection/', AgentForInspectionView.as_view(), name='agents-inspections'),
    path('send/', send_agent_report, name='send'),
    path('create/', AgentCreateView.as_view(), name='create-agent'),
]