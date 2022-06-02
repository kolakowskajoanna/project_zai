from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Adopter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'is_superuser', 'email', 'groups', 'id']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'id']


class AdopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = "__all__"
