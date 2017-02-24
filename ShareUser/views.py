from django.shortcuts import render
from .models import ShareUser
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
# Create your views here.

class ShareUserUpdateView(UpdateView):
    model = ShareUser
    fields = ['pushbullet_api_key', 'icon']

    def get_object(self):
        return get_object_or_404(ShareUser, pk=self.request.user.id)
