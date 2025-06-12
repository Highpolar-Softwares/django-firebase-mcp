"""
URL configuration for Firebase MCP app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mcp_handler, name='mcp_handler'),
]
