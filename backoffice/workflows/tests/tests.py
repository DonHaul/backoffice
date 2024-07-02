import vcr
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import get_resolver, reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Workflow, WorkflowTicket

User = get_user_model()


def list_all_view_names():
    resolver = get_resolver(None)
    all_view_names = set()

    # Iterate through all URL patterns
    for pattern in resolver.url_patterns:
        # Recursively traverse the resolver tree to find view names
        _list_all_view_names(pattern, all_view_names)

    return all_view_names


def _list_all_view_names(pattern, all_view_names):
    # If the pattern has a name, add it to the set of view names
    if hasattr(pattern, "name") and pattern.name is not None:
        all_view_names.add(pattern.name)

    # Recursively traverse the resolver tree for included URL patterns
    if hasattr(pattern, "url_patterns"):
        for sub_pattern in pattern.url_patterns:
            _list_all_view_names(sub_pattern, all_view_names)


class FetchWorkflowErrorTestCase(TestCase):

    fixtures = ["backoffice/fixtures/groups.json"]

    def setUp(self):
        # Create some test data
        self.api_client = APIClient()

        self.admin_group = Group.objects.get(name="admin")
        self.admin = User.objects.create_user(email="admin@test.com", password="12345")
        self.admin.groups.add(self.admin_group)

        self.api_client.force_authenticate(user=self.admin)

        self.workflow = Workflow.objects.create(url="https://unusedfield.com", data={}, core=False, is_update=False)
        self.ticket1 = WorkflowTicket.objects.create(ticket_id="ticket1", workflow_id=self.workflow)
        self.ticket2 = WorkflowTicket.objects.create(ticket_id="ticket2", workflow_id=self.workflow)

    def test_fetchworkflow_tickets(self):

        url = reverse("workflow_tickets_list", kwargs={"workflow_id": self.workflow.id})

        self.api_client.force_authenticate(user=self.admin)
        response = self.api_client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of tickets returned
        self.assertEqual(len(response.data), 2)
        # Check the content of the response
        self.assertEqual(response.data[0]["ticket_id"], self.ticket1.ticket_id)
        self.assertEqual(response.data[1]["ticket_id"], self.ticket2.ticket_id)

    @vcr.use_cassette("backoffice/workflows/tests/cassettes/test_restart_full_dagrun.yaml")
    def test_restart_full_dagrun(self):

        url = reverse(
            "workflow_restart",
            kwargs={
                "workflow_id": "0092dfb8-e754-46c2-b2f7-c4d116509107",
                "dag_id": "author_create_initialization_dag",
            },
        )

        response = self.api_client.post(url)
        self.assertEqual(response.status_code, 200)

    @vcr.use_cassette("backoffice/workflows/tests/cassettes/test_restart_a_task.yaml")
    def test_restart_a_task(self):
        url = reverse(
            "workflow_restart",
            kwargs={
                "workflow_id": "0092dfb8-e754-46c2-b2f7-c4d116509107",
                "dag_id": "author_create_initialization_dag",
            },
        )

        response = self.api_client.post(url, json={"task_ids": ["set_workflow_status_to_running"]})
        self.assertEqual(response.status_code, 200)

    @vcr.use_cassette("backoffice/workflows/tests/cassettes/test_restart_with_params.yaml")
    def test_restart_with_params(self):
        url = reverse(
            "workflow_restart",
            kwargs={
                "workflow_id": "0092dfb8-e754-46c2-b2f7-c4d116509107",
                "dag_id": "author_create_initialization_dag",
            },
        )

        response = self.api_client.post(url, json={"params": {"workflow_id": "0092dfb8-e754-46c2-b2f7-c4d116509107"}})
        self.assertEqual(response.status_code, 200)
