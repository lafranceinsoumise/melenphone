from rest_framework.serializers import ModelSerializer, SlugRelatedField, Serializer
from rest_framework import serializers

from .models import UserExtend
from .actions.callhub import create_agent, verify_agent
from accounts.models import User
from callcenter.exceptions import CallerValidationError
from django.db import IntegrityError


class UserSerializer(ModelSerializer):
    agentUsername = SlugRelatedField(slug_field='agentUsername', source='UserExtend', read_only=True)
    phi = SlugRelatedField(slug_field='phi', source='UserExtend', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'city', 'country_code', 'agentUsername', 'phi')
        read_only_fields = ('email', 'agentUsername', 'phi')


class UserExtendSerializer(ModelSerializer):
    class Meta:
        model = UserExtend
        fields = (
            'id', 'agentUsername', 'phi', 'phi_multiplier', 'first_call_of_the_day'
        )
        read_only_fields = (
            'id', 'phi', 'phi_multiplier', 'first_call_of_the_day'
        )

    def create(self, validated_data):
        user = validated_data['user']

        username = validated_data['agentUsername']

        create_agent(user, username)

        return UserExtend.objects.create(
            agentUsername=validated_data['agentUsername'],
            user=user
        )

class CallhubCredentialsSerializer(Serializer):
    agentUsername = serializers.CharField()
    password = serializers.CharField(write_only=True)
    phi = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        agentUsername = validated_data['agentUsername']
        password = validated_data['password']
        phi = 0

        verify_agent(agentUsername,password)

        try:
            return UserExtend.objects.create(
                agentUsername=validated_data['agentUsername'],
                phi=phi,
                user=validated_data['user']
            )
            #Solves the problem 'UserExtend has no attribute password'
            return {'agentUsername': agentUsername, 'password': password}
        except IntegrityError:
            raise CallerValidationError("Ce compte callhub est déjà associé à un compte du Mélenphone !",
                                          code='already_associated')