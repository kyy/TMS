from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    """Предоставление доступа управление тасками только автору"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author.id == request.user.id)
