from rest_framework import permissions


class IsOwnerOrPublicReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только владельцу редактировать свои привычки,
    но разрешающее всем читать публичные привычки.
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено для всех, если привычка публичная
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or obj.user == request.user

        # Запись разрешена только владельцу
        return obj.user == request.user
