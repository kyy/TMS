from rest_framework.permissions import BasePermission


class IsAnon(BasePermission):
    """
    Предоставление доступа только анонимным пользователям
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_anonymous)