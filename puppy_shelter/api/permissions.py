from rest_framework.permissions import BasePermission
from api.utils import is_adopion_owner, is_adopter_owner


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


class IsAdoptionOwner(BasePermission):
    message = 'Iz not Urz!'

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser: return True  # ! SU powinien moc to robic

        adoption_id = view.kwargs.get('pk')
        return is_adopion_owner(adoption_id, user)


class IsEmployeeOrOwner(BasePermission):
    message = 'Iz not Urz!'

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser: return True  # ! SU powinien moc to robic
        if user.groups.filter(name='employees').exists(): return True  # ! pracownik tez moze

        adoption_id = view.kwargs.get('pk')
        return is_adopter_owner(adoption_id, user)  # ! owner tez moze
