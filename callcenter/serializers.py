from rest_framework.serializers import ModelSerializer, RelatedField

from .models import UserExtend
from accounts.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('city', 'country_code')

class UserExtendSerializer(ModelSerializer):
    location = UserSerializer(source='user')

    class Meta:
        model = UserExtend
        fields = (
            'id', 'agentUsername', 'location', 'phi', 'phi_multiplier',
            'alltime_leaderboard', 'weekly_leaderboard', 'daily_leaderboard'
        )
        read_only_fields = (
            'id', 'phi', 'phi_multiplier' 'alltime_leaderboard',
            'weekly_leaderboard', 'daily_leaderboard'
        )

    def update(self, instance, validated_data):
        instance.agentUsername = validated_data.get('agentUsername', instance.agentUsername)
        instance.save()

        location = validated_data.get('location', None)
        user = instance.user
        if location is not None:
            user.city = location.get('city', user.city)
            user.country_code = location.get('country_code', user.country_code)
            user.save()

        return instance
