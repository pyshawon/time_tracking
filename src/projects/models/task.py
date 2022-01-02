from django.contrib.auth.models import User
from django.db import models
from projects.models.project import Project


class Task(models.Model):
    """
    Represent project tasks with task informations.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    dateline = models.DateTimeField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_tasks')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks')

    mark_as_done = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Tasks"
        ordering = ['-id']

    def __str__(self):
        return self.name
