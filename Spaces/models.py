from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Space(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(to=User, related_name="%(app_label)s_%(class)s_related")
    added_users = models.ManyToManyField(to=User)


class SharedItem(models.Model):
    url = models.CharField(max_length=1000)
    text = models.TextField(blank=True)
    shared_by = models.ForeignKey(to=User)
    shared_at = models.DateTimeField(auto_now_add=True)
    space = models.ForeignKey(to=Space)


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(to=User)
    created = models.DateTimeField(auto_created=True)
    shared_item = models.ForeignKey(to=SharedItem)