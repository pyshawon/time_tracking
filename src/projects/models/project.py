from django.db import models
from django.contrib.auth.models import User
from projects.utils.choices import PROJECT_STATUS


class Project(models.Model):
    """
    Project Model represent different type of the project.
    """
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='own_projects')
    users = models.ManyToManyField(User, related_name='assign_projects')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=PROJECT_STATUS, default="ongoing")
    start_datetime = models.DateTimeField()
    dateline = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"
        ordering = ['-id']
