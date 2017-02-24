from django.shortcuts import render
from .models import ShareUser
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets
from ShareUser.serializer import ShareUserSerializer, UserSerializer
# Create your views here.

class ShareUserUpdateView(UpdateView):
    model = ShareUser
    fields = ['pushbullet_api_key', 'icon']

    def get_object(self):
        return get_object_or_404(ShareUser, pk=self.request.user.id)


class ShareUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ShareUser.objects.all()
    serializer_class = ShareUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
