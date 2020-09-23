from .models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize profile data"""
    subscriptions = serializers.ListField(
            child=serializers.CharField(max_length=100))

    class Meta:
        model = Profile
        fields = ['subscriptions']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize user's data; if POST then create new user profile"""
    subscriptions = serializers.ListField(source='profile.subscriptions')

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'subscriptions']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """create new user profile"""
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data.pop('password')
            )
        subscriptions = validated_data['profile']['subscriptions']
        Profile.objects.create(user=user,
                               subscriptions=subscriptions)

        return user

    def update(self, instanse, validated_data):
        """update user profile"""
        profile_data = validated_data.pop('profile', {})
        subscriptions = profile_data.get('subscriptions')

        instanse.username = validated_data.get('username', instanse.username)
        instanse.save()

        profile = instanse.profile

        if profile_data and subscriptions:
            profile.subscriptions = subscriptions
            profile.save()

        return instanse
