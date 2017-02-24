
from rest_framework import routers, serializers, viewsets
from ShareUser.serializer import ShareUserSerializer
from .models import Space

class SpaceSerializer(serializers.HyperlinkedModelSerializer):
    owner = ShareUserSerializer()
    added_users = ShareUserSerializer(many=True)

    class Meta:
        model = Space
        fields = ('url', 'name',  'owner', 'added_users')
