from django.urls import include, path
from . import views

urlpatterns = [
    path('/workflows/<str:workflow_id>/tickets/', views.WorkflowTicketList.as_view(), name='workflow_tickets_list'),
]