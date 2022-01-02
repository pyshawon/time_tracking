
from django.http import request
from rest_framework import serializers
from projects.models import Project, Task
from auth.serializers import UserSerializer
from django.utils import timezone

from projects.utils.helper import date_diff


class TaskListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_time = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_status(self, obj):
        """
        Method for task status(Completed or Under Development) by 
        using mark_as_done flag.
        """
        return "Completed" if obj.mark_as_done else "Under Development"

    def get_total_time(self, obj):
        """
        Method for total time assigned for the task.
        """
        return date_diff(obj.dateline, obj.start_datetime)

    def get_time_left(self, obj):
        """
        Method for time left to Completed the task.
        """
        return date_diff(obj.dateline, timezone.now())

    def validate(self, data):
        """
        Check the view access for task. if requested user is 
        staff user or project owner or assigned user for this task can view the task.
        """
        if not self.context['request'].user.is_staff or \
            not self.context['request'].user == data['project'].owner or \
                not self.context['request'].user in data['project'].users.all():
            raise serializers.ValidationError(
                "Requested user are not alowed to view this tasks")

        return data


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data):
        """
        Check the create access for task.
        Only staff user and project owner can create task for a project.
        """
        if not self.context['request'].user.is_staff or \
                not self.context['request'].user == data['project'].owner:
            raise serializers.ValidationError(
                "Requested user are not alowed to create task")

        """
        Check the task start datetime or dateline is 
        less then project dateline.
        """
        if data['start_datetime'] > data['project'].dateline or \
                data['dateline'] > data['project'].dateline:
            raise serializers.ValidationError(
                "Task start datetime or dateline should be less then project dateline")

        """
        Check the selected task user is assigned in the project.
        """
        if not data['user'] in data['project'].users.all():
            raise serializers.ValidationError(
                "Selected Used not is not assigned in this project")

        """
        Check the start_datetime should be less than dateline.
        """

        if data['start_datetime'] > data['dateline']:
            raise serializers.ValidationError(
                "Start datetime should be less than dateline")

        return data


class ProjectListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True)
    total_time = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_total_time(self, obj):
        """
        Method for total time assigned for the project.
        """
        return date_diff(obj.dateline, obj.start_datetime)

    def get_time_left(self, obj):
        """
        Method for time left to Completed the project.
        """
        return date_diff(obj.dateline, timezone.now())


class ProjectCretaeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def validate(self, data):
        """
        Check that Start datetime should be less than dateline.
        """
        if data['start_datetime'] > data['dateline']:
            raise serializers.ValidationError(
                "Start datetime should be less than dateline")

        return data
