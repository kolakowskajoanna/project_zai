from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Adopter
from api.models import Adoption
from api.models import Puppy


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'is_superuser', 'email', 'groups', 'id']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'id']


class AdopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = "__all__"


class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = "__all__"


class PuppySerializer(serializers.ModelSerializer):
    class Meta:
        model = Puppy
        fields = "__all__"
