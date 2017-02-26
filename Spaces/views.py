from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
import requests
import http.client, urllib
from ShareUser.models import *
from .forms import SharedItemForm
import re
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from PIL import Image
from .image_helpers import get_page_text
from io import BytesIO

# Create your views here.

class SpacesListView(ListView):
    model = Space

    def get_queryset(self):
        s_user = ShareUser.objects.filter(user=self.request.user)
        return Space.objects.filter(Q(owner=s_user) | Q(added_users__in=[s_user]))


class SpacesCreateView(CreateView):
    model = Space
    fields = ['name', 'added_users']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.owner = self.request.user
        return super(CreateView, self).form_valid(form)


class SpacesUpdateView(UpdateView):
    model = Space
    fields = ['name', 'added_users']


class SharedItemListView(ListView):
    model = SharedItem
    paginate_by = 10

    def get_queryset(self):
        return SharedItem.objects.filter(space=self.get_space_id()).order_by('-shared_at')

    def get_space_id(self):
        return 1 if not 'space_id' in self.kwargs else self.kwargs['space_id']

    def get_context_data(self, **kwargs):
        context = super(SharedItemListView, self).get_context_data(**kwargs)
        space = Space.objects.get(id=self.get_space_id())
        context['space'] = space
        context['share_users'] = list(space.added_users.all())
        context['share_users'].append(space.owner)
        context['form'] = SharedItemForm()
        return context


class SharedItemDetailView(DetailView):
    model = SharedItem

    def get_context_data(self, **kwargs):
        context = super(SharedItemDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(shared_item=self.object)
        return context


class SharedItemCreateView(CreateView):
    model = SharedItem
    form_class = SharedItemForm

    def form_valid(self, form):
        form.instance.shared_by = ShareUser.objects.get(user=self.request.user)
        form.instance.space = Space.objects.get(id=self.kwargs['space_id'])
        return super(CreateView, self).form_valid(form)


class CommentCreateView(CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = ShareUser.objects.get(user=self.request.user)
        form.instance.shared_item = SharedItem.objects.get(id=self.kwargs['shareditem_id'])
        return super(CreateView, self).form_valid(form)
