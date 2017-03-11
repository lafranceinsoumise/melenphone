from rest_framework.serializers import ModelSerializer, RelatedField, ValidationError

from .models import UserExtend
from accounts.models import User
from django.conf import settings

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
        print(instance.pk)
        instance.agentUsername = validated_data.get('agentUsername', instance.agentUsername)
        instance.save()

        location = validated_data.get('location', None)
        user = instance.user
        if location is not None:
            user.city = location.get('city', user.city)
            user.country_code = location.get('country_code', user.country_code)
            user.save()

        if instance.pk is None: #On cree le user
            print('lol')
            token = 'Token ' + settings.CALLHUB_API_KHEY
            headers = {'Authorization': token }
            callhubData = {'username':validated_data.get('agentUsername', instance.agentUsername), 'email':user.email, 'team':'tout_le_monde'}

            r = requests.post('https://api.callhub.io/v1/agents/', data=callhubData, headers=headers) #On fait la requete sur l'API de github
            if r.status_code == requests.codes.created: #Si tout s'est bien passé
                #On enregistre le UserExtend dans la bdd
                    instance.agentUsername = validated_data.get('agentUsername', instance.agentUsername)
                    instance.save()

            elif r.status_code == 400: #Bad request : le username existe déjà !
                raise ValidationError("Un agent Callhub porte déjà ce nom.")

            else: #Autre erreur de callhub
                raise ValidationError("Callhub ne répond pas. Réessayez plus tard !")


        return instance
