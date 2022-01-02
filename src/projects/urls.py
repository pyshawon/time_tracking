from django.urls import path
from .views import (
    ProjectList,
    ProjectCreate,
    ProjectDetails,
    ProjectUpdate,
    TaskList,
    TaskCreate,
    TaskDetails,
    TaskUpdate
)

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='projects'),
    path('project-create/', ProjectCreate.as_view(), name='project-create'),
    path('project-update/<int:pk>/',
         ProjectUpdate.as_view(), name='project-update'),
    path('project-details/<int:pk>/',
         ProjectDetails.as_view(), name='project-details'),

    path('tasks/', TaskList.as_view(), name='home'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-details/<int:pk>/',
         TaskDetails.as_view(), name='task-update'),
    path('task-update/<int:pk>/',
         TaskUpdate.as_view(), name='task-details'),
]
