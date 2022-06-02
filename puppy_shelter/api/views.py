from django.shortcuts import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response as JSONResponse
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer
from api.models import Adopter
from api.serializers import AdopterSerializer
from rest_framework.decorators import api_view

# Create your views here.


def ping(request):
    return HttpResponse('Pong !!! 🚀')


@api_view()
def list_users(request):
    query = request.query_params.get('query')
    if query is None: return JSONResponse(data={"msg": "U fool!"}, status=400)
    # todo: jak to pociagnac dalej ? jak zaaplikowac query na kwargi do .filter(**query)
    users = User.objects.filter(username__contains=query)
    response = [{'username': e.username} for e in users]
    return JSONResponse(data=response, status=200)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdopterViewSet(viewsets.ModelViewSet):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    permission_classes = [permissions.IsAuthenticated]
