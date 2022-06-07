from django.contrib.auth.models import User, Group
 
 
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer
from api.serializers import AdopterSerializer
 
from api.models import Adoption, Adopter, Puppy
from api.serializers import AdoptionEmployeeSerializer, AdoptionUserSerializer, AdopterCreateUpdateSerializer
from api.serializers import PuppySerializer, UserCreateSerializer
 
from api.permissions import IsEmployee, IsSuperuser, IsAdoptionOwner, IsEmployeeOrOwner
from api.utils import is_employee, is_super_user
from api.utils import booly
from api.viewsets import ViewSet
 
 
class UserViewSet(ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]
    filter_type_map = {
        'is_superuser': booly
    }
 
    action_permissions = {
        'list': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAuthenticated],
        'update': [permissions.IsAuthenticated, IsSuperuser],
        'partial_update': [permissions.IsAuthenticated, IsSuperuser],
        'destroy': [permissions.IsAuthenticated, IsSuperuser]
    }
 
    def get_serializer(self, *args, **kwargs):
        action = self.action or 'list'
        if is_super_user(self.request.user) : return super().get_serializer(*args, **kwargs)
        if action != 'create': return super().get_serializer(*args, **kwargs)
 
        serializer_class = UserCreateSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
 
 
class GroupViewSet(ViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    default_permissions = [IsSuperuser]
 
 
class AdopterViewSet(ViewSet):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    permission_classes = [permissions.IsAuthenticated]
    default_permissions = [permissions.IsAuthenticated]
    action_permissions = {
        'retrieve': [IsEmployeeOrOwner],
        'update': [IsEmployeeOrOwner],
        'partial_update': [IsEmployeeOrOwner],
        'destroy': [IsEmployee]
    }
 
    def get_serializer(self, *args, **kwargs):
        if self.action not in ['update', 'partial_update', 'create']: return super().get_serializer(*args, **kwargs)
 
        if is_employee(self.request.user) or is_super_user(self.request.user): serializer_class = AdopterSerializer
        else: serializer_class = AdopterCreateUpdateSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
 
 
class AdoptionEmployeeViewSet(ViewSet):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]
    filter_type_map = {
        'adopter': int,
        'created_by': int,
    }
    default_permissions = [IsEmployee]
 
 
class AdoptionUserViewSet(ViewSet):
    http_method_names = ['get', 'options']
    queryset = Adoption.objects.all()
    serializer_class = AdoptionUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]
    filter_type_map = {
        'adopter': int,
        'created_by': int,
    }
    default_permissions = [permissions.IsAuthenticated]
    action_permissions = {
        'retrieve': [IsAdoptionOwner],
    }
 
    def get_queryset(self):
        base_q = super().get_queryset()
        action = self.action or 'list'
        if action != 'list': return base_q
        return base_q.filter(adopter__user=self.request.user)
 
 
class PuppyViewSet(ViewSet):
    queryset = Puppy.objects.all()
    serializer_class = PuppySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_type_map = {
        'age': int,
        'adoption': int,
    }
    action_permissions = {
        'create': [permissions.IsAuthenticated, IsEmployee],
        'update': [permissions.IsAuthenticated, IsEmployee],
        'partial_update': [permissions.IsAuthenticated, IsEmployee],
        'destroy': [permissions.IsAuthenticated, IsEmployee]
    }
 