from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from projects.models import Project


class ProjectTests(APITestCase):
    def setUp(self):
        staff_user = User.objects.create_user(
            username="testuser_staff",
            password="admin@123",
            is_staff=True
        )
        normal_user = User.objects.create_user(
            username="testuser",
            password="admin@123"
        )

    def test_token(self):
        """
        Ensure that user token is created.
        """
        staff_user_token = Token.objects.get(user__username='testuser_staff')
        normal_user_token = Token.objects.get(user__username='testuser')

        self.assertIsNotNone(staff_user_token)
        self.assertIsNotNone(normal_user_token)

    def test_create_project_with_staff_user(self):
        """
        Ensure we can create a new project with Staff User.
        """
        staff_user_token = Token.objects.get(user__username='testuser_staff')

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + staff_user_token.key)
        url = reverse('project-create')

        data = {
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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'Project')

    def test_create_project_with_normal_user(self):
        """
        Ensure that Normal User can not create project.
        """
        normal_user_token = Token.objects.get(user__username='testuser')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + normal_user_token.key)
        url = reverse('project-create')

        data = {
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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_validate_project_datetime(self):
        """
        Check that Start datetime should be less than dateline.
        """
        staff_user_token = Token.objects.get(user__username='testuser_staff')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + staff_user_token.key)
        url = reverse('project-create')

        data = {
            "name": "Project",
            "description": "Project 1",
            "status": "ongoing",
            "start_datetime": "2022-01-02T11:18:12.019Z",
            "dateline": "2020-03-02T11:18:12.019Z",
            "owner": 1,
            "users": [
                1
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertListEqual(response.data['non_field_errors'], [ErrorDetail(
            string='Start datetime should be less than dateline', code='invalid')])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
