from rest_framework import permissions
class canChangeProfile(permissions.BasePermission):
    message="you can not change the profile"
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # if request.user.pk==obj.