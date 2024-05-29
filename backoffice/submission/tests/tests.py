from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient
import vcr

User = get_user_model()

class FetchWorkflowErrorTestCase(TestCase):

    fixtures = ["backoffice/fixtures/groups.json"]

    def setUp(self):
        # Create some test data
        self.api_client = APIClient()
        
        self.admin_group = Group.objects.get(name="admin")
        self.admin = User.objects.create_user(email="admin@test.com", password="12345")
        self.admin.groups.add(self.admin_group)

    @vcr.use_cassette('backoffice/submission/tests/cassettes/fetchworkflowerror.yaml')
    def test_fetchworkflowerror(self):

        # Define the parameters
        params = {'workflow_id': '0092dfb8-e754-46c2-b2f7-c4d116509107'}

        self.api_client.force_authenticate(user=self.admin)
        #response = self.api_client.get(reverse('submission-fetchworkflowerror'), params)
        response = self.api_client.get(reverse('submission-fetchworkflowerror'), params)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertIn('set_workflow_status_to_running',response.json()['tracebacks'])