from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from ShareUser.models import *
from ShareSpaces.settings import ALLOWED_HOSTS
# Create your models here.


class Space(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(to=ShareUser, related_name="%(app_label)s_%(class)s_related")
    added_users = models.ManyToManyField(to=ShareUser)


class SharedItem(models.Model):
    url = models.CharField(max_length=1000)
    text = models.TextField(blank=True)
    shared_by = models.ForeignKey(to=ShareUser)
    shared_at = models.DateTimeField(auto_now_add=True)
    space = models.ForeignKey(to=Space)

    def get_absolute_url(self):
        host = 'localhost' if len(ALLOWED_HOSTS) is 0 else ALLOWED_HOSTS[0]
        return 'https://{0}{1}'.format(host, reverse('shared-item-detail', kwargs={'space_id': self.space.id, 'pk': self.pk}))

@receiver(post_save, sender=SharedItem)
def send_notification_to_all(sender, instance, created, **kwargs):
    for user in instance.space.added_users.all():
        s_user = user
        s_user.send_notification(instance)

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(to=ShareUser)
    created = models.DateTimeField(auto_now_add=True)
    shared_item = models.ForeignKey(to=SharedItem)

    def get_absolute_url(self):
        return self.shared_item.get_absolute_url()

@receiver(post_save, sender=Comment)
def send_notification_to_all(sender, instance, created, **kwargs):
    instance.text = '{0} says: {1}'.format(instance.user, instance.text)
    for user in instance.shared_item.space.added_users.all():
        s_user = user
        s_user.send_notification(instance)
