from django.urls import path

from main.apps import MainConfig
from main.views import HomeView, AgentListView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('agents/', AgentListView.as_view(), name='agents-list'),
]