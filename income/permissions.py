from rest_framework.permissions import BasePermission
# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.owner == request.user

