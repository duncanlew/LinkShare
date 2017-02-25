
from rest_framework import routers, serializers, viewsets
from ShareUser.serializer import ShareUserSerializer
from .models import Space, SharedItem

class SpaceSerializer(serializers.HyperlinkedModelSerializer):
    owner = ShareUserSerializer()
    added_users = ShareUserSerializer(many=True)

    class Meta:
        model = Space
        fields = ('url', 'pk', 'name',  'owner', 'added_users')

class SharedItemSerializer(serializers.HyperlinkedModelSerializer):
    shared_by = ShareUserSerializer()
    space = SpaceSerializer()

    class Meta:
        model = SharedItem
        fields = ('url', 'pk', 'text',  'shared_by', 'shared_at', 'space')
