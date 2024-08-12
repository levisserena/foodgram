from rest_framework.permissions import BasePermission


class IsAdminOrAuthor(BasePermission):
    """Проверка прав на авторство или администратора."""

    message = 'Нужны права администратора, модератора или автора'

    def has_object_permission(self, request, view, obj):
        """Разрешение на уровне объекта.

        Разрешает редактировать объект его владельцам и админам.
        Предполагается, что экземпляр модели имеет атрибут `author`.
        """
        return request.user == obj.author or request.user.is_superuser
