from rest_framework.permissions import BasePermission


class Public(BasePermission):
    def has_permission(self, request, view): return True


class IsSuperuser(BasePermission):
    message = 'SU only !!!'

    def has_permission(self, request, view): return request.user.is_superuser


class IsEmployee(BasePermission):
    message = 'Only for employees sorii'

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser: return True  # ! SU powinien moc to robic

        return user.groups.filter(name='employees').exists()
