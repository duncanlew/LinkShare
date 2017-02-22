from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import requests
import http.client, urllib
# Create your views here.

class SpacesListView(ListView):
    model = Space

    def get_queryset(self):
        return Space.objects.filter(Q(owner=self.request.user) | Q(added_users__in=[self.request.user]))


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
        # Call the base implementation first to get a context
        context = super(SharedItemListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['space'] = self.get_space_id()
        return context


class SharedItemCreateView(CreateView):
    model = SharedItem
    fields = ['url', 'text']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if not form.instance.text:
            form.instance.text = get_title_from_url(form.instance.url)
        form.instance.shared_by = self.request.user
        form.instance.space = Space.objects.get(id=self.kwargs['space_id'])
        return super(CreateView, self).form_valid(form)


def get_title_from_url(url):
    try:
        headers = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        n = requests.get(url, headers=headers)
        al = n.text
        return al[al.find('<title>') + 7: al.find('</title>')]
    except Exception as e:
        print(e)


def send_notification_to_added_users(user_key, message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": "APP_TOKEN",
                     "user": "USER_KEY",
                     "message": message,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()
