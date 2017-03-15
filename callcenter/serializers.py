from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import UserExtend
from .actions.callhub import create_agent
from accounts.models import User

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
