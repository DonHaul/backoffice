from django.urls import path

from . import views

urlpatterns = [
    path(
        "workflows/<str:dag_id>/<str:workflow_id>/restart",
        views.RestartWorkflowView.as_view(),
        name="workflow_restart",
    ),
]
