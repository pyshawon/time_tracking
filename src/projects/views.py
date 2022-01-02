from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from projects.utils.permissions import IsStaffUser
from rest_framework import generics
from projects.models import Task, Project
from projects.serializers import (
    ProjectListSerializer,
    ProjectCretaeSerializer,
    TaskListSerializer,
    TaskCreateSerializer
)


class ProjectCreate(generics.CreateAPIView):
    """
    Create API View for Create Project.
    """
    queryset = Project.objects.select_related(
        'owner').prefetch_related('users').all()
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = ProjectCretaeSerializer


class ProjectList(generics.ListAPIView):
    """
    List API View for Project Lists.
    """
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        """
        Check Staff User or Project Owner and Assigned usser.
        Staff User can see all the Projects and 
        Project Owner and Assigned usser can the there Projects
        """
        if self.request.user.is_staff:
            return Project.objects.select_related('owner').prefetch_related('users').all()
        return Project.objects.select_related('owner').prefetch_related('users').filter(
            Q(owner=self.request.user) |
            Q(users=self.request.user)
        ).distinct()


class ProjectDetails(generics.RetrieveAPIView):
    """
    Retrieve API View for Project Details.
    """
    queryset = Project.objects.select_related(
        'owner').prefetch_related('users').all()
    serializer_class = ProjectListSerializer


class ProjectUpdate(generics.UpdateAPIView):
    """
    Update API View for Project Update.
    """
    queryset = Project.objects.select_related(
        'owner').prefetch_related('users').all()
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = ProjectCretaeSerializer


class TaskList(generics.ListAPIView):
    """
    List API View for Task List.
    """
    serializer_class = TaskListSerializer

    def get_queryset(self):
        """
        Check Staff User or Project Owner and Assigned usser.
        Staff User can see all the tasks and 
        Project Owner and Assigned usser can the there project tasks
        """
        if self.request.user.request.user.is_staff:
            return Task.objects.select_related('project', 'project__users', 'project__owner', 'user').all()
        return Task.objects.select_related('project', 'project__users', 'project__owner', 'user').filter(
            Q(user=self.request.user) |
            Q(project__owner=self.request.user) |
            Q(project__users=self.request.user)
        ).distinct()


class TaskCreate(generics.CreateAPIView):
    """
    Create API View for Task Create.
    """
    queryset = Task.objects.select_related('project', 'user').all()
    serializer_class = TaskCreateSerializer


class TaskDetails(generics.RetrieveAPIView):
    """
    Retrieve API View for Task Details.
    """
    queryset = Task.objects.select_related('project', 'user').all()
    serializer_class = TaskListSerializer


class TaskUpdate(generics.UpdateAPIView):
    """
    Update API View for Task Update.
    """
    queryset = Task.objects.select_related('project', 'user').all()
    serializer_class = TaskCreateSerializer
