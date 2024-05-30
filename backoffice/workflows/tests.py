from django.apps import apps
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Workflow, WorkflowTicket
from django.contrib.auth import get_user_model


User = get_user_model()
# Workflow = apps.get_model(app_label="workflows", model_name="Workflow")
# WorkflowTicket = apps.get_model(app_label="workflows", model_name="WorkflowTicket")

class FetchWorkflowErrorTestCase(TestCase):

    fixtures = ["backoffice/fixtures/groups.json"]

    def setUp(self):
        # Create some test data
        self.api_client = APIClient()

        self.admin_group = Group.objects.get(name="admin")
        self.admin = User.objects.create_user(email="admin@test.com", password="12345")
        self.admin.groups.add(self.admin_group)

        self.workflow = Workflow.objects.create(url='https://unusedfield.com',data={},core=False,is_update=False)
        self.ticket1 = WorkflowTicket.objects.create(ticket_id='ticket1',workflow_id=self.workflow)
        self.ticket2 = WorkflowTicket.objects.create(ticket_id='ticket2',workflow_id=self.workflow)

    def test_fetchworkflow_tickets(self):


        url = reverse('workflow_tickets_list', kwargs={'workflow_id': self.workflow.id})

        self.api_client.force_authenticate(user=self.admin)
        response = self.api_client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of tickets returned
        self.assertEqual(len(response.data), 2)
        # Check the content of the response
        self.assertEqual(response.data[0]['ticket_id'], self.ticket1.ticket_id)
        self.assertEqual(response.data[1]['ticket_id'], self.ticket2.ticket_id)