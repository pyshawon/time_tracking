from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """
    Permission to only Staff User can create Project.
    """

    def has_permission(self, request, view):
        return True if request.user.is_staff else False
