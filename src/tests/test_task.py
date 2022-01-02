from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from projects.models import Task


class TaskTests(APITestCase):
    def setUp(self):
        self.project_create_url = reverse('project-create')
        self.task_create_url = reverse('task-create')

        self.project_data_sample = {
            "name": "Project",
            "description": "Project 1",
            "status": "ongoing",
            "start_datetime": "2022-01-01T11:18:12.019Z",
            "dateline": "2022-10-01T11:18:12.019Z",
            "owner": 1,
            "users": [
                1
            ]
        }

        self.task_data_sample = {
            "name": "task 1",
            "description": "Demo Task",
            "start_datetime": "2022-01-02T14:52:26.224Z",
            "dateline": "2022-04-02T14:52:26.224Z",
            "mark_as_done": True,
            "user": 1,
            "project": 1
        }

        assigned_user = User.objects.create_user(
            username="testuser_assigned",
            password="admin@123",
            is_staff=True
        )
        other_user = User.objects.create_user(
            username="testuser",
            password="admin@123"
        )
        assigned_user_token = Token.objects.get(
            user__username='testuser_assigned')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + assigned_user_token.key)

    def test_create_project_tasks(self):
        """
        Ensure that User can create task.
        """
        project_response = self.client.post(self.project_create_url,
                                            self.project_data_sample, format='json')
        response = self.client.post(
            self.task_create_url, self.task_data_sample, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, 'task 1')

    def test_validate_task_datetime(self):
        """
        Check the task start datetime or dateline is 
        less then project dateline.
        """
        self.project_data_sample = {
            "name": "Project",
            "description": "Project 1",
            "status": "ongoing",
            "start_datetime": "2022-01-02T11:18:12.019Z",
            "dateline": "2022-03-02T11:18:12.019Z",
            "owner": 1,
            "users": [
                1
            ]
        }

        self.task_data_sample = {
            "name": "task 1",
            "description": "Demo Task",
            "start_datetime": "2022-01-02T14:52:26.224Z",
            "dateline": "2022-04-02T14:52:26.224Z",
            "mark_as_done": True,
            "user": 1,
            "project": 1
        }
        project_response = self.client.post(self.project_create_url,
                                            self.project_data_sample, format='json')
        response = self.client.post(
            self.task_create_url, self.task_data_sample, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(response.data['non_field_errors'], [ErrorDetail(
            string='Task start datetime or dateline should be less then project dateline', code='invalid')])
