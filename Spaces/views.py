from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
import requests
import http.client, urllib
from ShareUser.models import *
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
        context = super(SharedItemListView, self).get_context_data(**kwargs)
        space = Space.objects.get(id=self.get_space_id())
        users = space.added_users.all()
        context['space'] = space
        context['share_users'] = list(ShareUser.objects.filter(user__in=users))
        context['share_users'].append(ShareUser.objects.get(user=space.owner))
        return context

class SharedItemDetailView(DetailView):
    model = SharedItem

    def get_context_data(self, **kwargs):
        context = super(SharedItemDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(shared_item=self.object)
        return context

class SharedItemCreateView(CreateView):
    model = SharedItem
    fields = ['url', 'text']

    def form_valid(self, form):
        if not form.instance.text:
            form.instance.text = get_title_from_url(form.instance.url)[:50]
        form.instance.shared_by = self.request.user
        form.instance.space = Space.objects.get(id=self.kwargs['space_id'])
        return super(CreateView, self).form_valid(form)

class CommentCreateView(CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.shared_item = SharedItem.objects.get(id=self.kwargs['shareditem_id'])
        return super(CreateView, self).form_valid(form)

def get_title_from_url(url):
    try:
        headers = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        n = requests.get(url, headers=headers)
        al = n.text
        return al[al.find('<title>') + 7: al.find('</title>')]
    except Exception as e:
        print(e)
