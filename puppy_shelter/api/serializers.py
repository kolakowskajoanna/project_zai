from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Adopter
from api.models import Adoption
from api.models import Puppy
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError

from api.utils import is_adopter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'email', 'groups', 'id']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'id']


class AdopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = "__all__"


class AdopterCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Dla regular usera (nie SU, nie emplyee)
    """
    class Meta:
        model = Adopter
        exclude = ["user"]

    def create(self, validated_data):
        user = self.context['request'].user
        if is_adopter(user):  # ! jesli jest juz adopterem to blokujemy
            raise ValidationError(detail={
                "user": [
                    "This field must be unique."
                ]
            })
        adopter = Adopter(**validated_data)
        adopter.user_id = user.id
        try:
            adopter.save()
        except IntegrityError as e: raise ValidationError(detail={"msg": f"Failed! :( {repr(e)}"})
        return adopter


class AdoptionEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = "__all__"


class AdoptionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = "__all__"


class PuppySerializer(serializers.ModelSerializer):
    class Meta:
        model = Puppy
        fields = "__all__"
