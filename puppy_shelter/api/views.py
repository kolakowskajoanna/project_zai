from typing import Any
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response as JSONResponse
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer
from api.models import Adopter
from api.serializers import AdopterSerializer
from rest_framework.decorators import api_view

from api.models import Adoption
from api.serializers import AdoptionSerializer
from api.models import Puppy
from api.serializers import PuppySerializer

from django.core.exceptions import FieldError
from rest_framework.exceptions import ValidationError
from api.permissions import IsEmployee, IsSuperuser, Public



class ViewSet(viewsets.ModelViewSet):  # ! wyjac to
    default_filter_type_map = {
        'id': int
    }
    filter_type_map = dict()  # ! <- nadpisuje klasa dziedziczaca :)
    action_permissions = {    # ! <- nadpisuje klasa dziedziczaca :)
        'list': [permissions.IsAuthenticated],
        'create': list(),     # ! klasa dziedziczaca nie moze zostawiac pustych permissionow !!!
        'retrieve': [permissions.IsAuthenticated],
        'update': list(),
        'partial_update': list(),
        'destroy': list()
    }

    def get_queryset(self):
        # ! custom filtrowanie po query params
        query_params = self.request.query_params
        filters = dict()
        type_map = self.default_filter_type_map | self.filter_type_map  # ! zlacz slowniki
        for field_name, field_value in query_params.items():
            if not field_value:  # ! jestli param= to null / None
                filters[field_name] = None
            elif '__in' in field_name:  # ! jesli mamy field_id__in=1,2  ect
                filters[field_name] = field_value.split(',')
            else:
                filters[field_name] = type_map.get(field_name, str)(field_value)  # ! castujemy str / int ect. <- z mapowania
        try:
            return self.serializer_class.Meta.model.objects.filter(**filters) # ! self.serializer_class.Meta.model < klasa z modelem orm
        except FieldError as e:
            raise ValidationError(detail={"msg": f"Field error -> {repr(e)}"}) # ! jesli cos nie tak to 400 -> err

    def get_permissions(self):
        action = self.action or 'list'
        permissions = [p() for p in self.action_permissions.get(action)]
        if not permissions: raise EnvironmentError(f'No permissions provied for "{self.__class__.__name__} action: {action}"')
        return permissions


def booly(value: str) -> bool:  # ! wyjac to
    v = value.lower()
    if v == 'false': return False
    if v == 'true': return True
    if v == '0': return False
    if v == '1': return True
    raise ValidationError(
        detail={
            "msg": f"Invalid boolean filter value: '{value}', boolean filters must use [0, 1, true, false] u noob"
        }
    )



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
        'create': [Public],
        'retrieve': [permissions.IsAuthenticated],
        'update': [permissions.IsAuthenticated, IsSuperuser],
        'partial_update': [permissions.IsAuthenticated, IsSuperuser],
        'destroy': [permissions.IsAuthenticated, IsSuperuser]
    }



class GroupViewSet(ViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    action_permissions = {
        'list': [permissions.IsAuthenticated],
        'create': [permissions.IsAuthenticated, IsSuperuser],
        'retrieve': [permissions.IsAuthenticated],
        'update': [permissions.IsAuthenticated, IsSuperuser],
        'partial_update': [permissions.IsAuthenticated, IsSuperuser],
        'destroy': [permissions.IsAuthenticated, IsSuperuser]
    }


class AdopterViewSet(ViewSet):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    permission_classes = [permissions.IsAuthenticated]
    action_permissions = {
        'list': [permissions.IsAuthenticated],
        'create': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAuthenticated],
        'update': [permissions.IsAuthenticated, IsEmployee],
        'partial_update': [permissions.IsAuthenticated, IsEmployee],
        'destroy': [permissions.IsAuthenticated, IsEmployee]
    }


class AdoptionViewSet(ViewSet):  # ! todo: moze dodac osobny adoption view dla adopterow
    # ! dla emplyerow
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]
    filter_type_map = {
        'adopter': int,
        'created_by': int,
    }
    # default_permissions = [permissions.IsAuthenticated, IsEmployee]  # ! todo - refaktor jak beda checi
    action_permissions = {
        'list': [permissions.IsAuthenticated, IsEmployee],
        'create': [permissions.IsAuthenticated, IsEmployee],
        'retrieve': [permissions.IsAuthenticated, IsEmployee],
        'update': [permissions.IsAuthenticated, IsEmployee],
        'partial_update': [permissions.IsAuthenticated, IsEmployee],
        'destroy': [permissions.IsAuthenticated, IsEmployee]
    }


class PuppyViewSet(ViewSet):
    queryset = Puppy.objects.all()
    serializer_class = PuppySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_type_map = {
        'age': int,
        'adoption': int,
    }
    action_permissions = {
        'list': [Public],
        'create': [permissions.IsAuthenticated, IsEmployee],
        'retrieve': [Public],
        'update': [permissions.IsAuthenticated, IsEmployee],
        'partial_update': [permissions.IsAuthenticated, IsEmployee],
        'destroy': [permissions.IsAuthenticated, IsEmployee]
    }
