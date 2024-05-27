from django.urls import path

from main.apps import MainConfig
from main.views import (HomeView, AgentListView, AgentForInspectionView, send_agents_report,
                        AgentCreateView, AgentPendingConfirmationView, AgentDetailView, AgentUpdateView,
                        AgentWithExpired,send_email_agents_ex)

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='index'),

    path('agents/', AgentListView.as_view(), name='agents-list'),
    path('create/', AgentCreateView.as_view(), name='create-agent'),
    path('detail/<int:pk>/', AgentDetailView.as_view(), name='agent-detailt'),
    path('update/<int:pk>/', AgentUpdateView.as_view(), name='agent-update'),
    path('inspection/', AgentForInspectionView.as_view(), name='agents-inspections'),
    path('send/', send_agents_report, name='send'),

    path('under_inspection/', AgentPendingConfirmationView.as_view(), name='under_inspection'),
    path('expired/', AgentWithExpired.as_view(), name='expired_inspection'),
    path('send_expired/', send_email_agents_ex, name='send_email_agents_ex'),
]
