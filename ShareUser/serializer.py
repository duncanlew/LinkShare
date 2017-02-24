from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ShareUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class ShareUserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )

    class Meta:
        model = ShareUser
        fields = ('user', 'icon',)
