from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from pushbullet import Pushbullet

# Create your models here.

class ShareUser(models.Model):
    pushbullet_api_key = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(to=User)

    def send_notification(self, shared_item):
        pb = Pushbullet(self.pushbullet_api_key)
        push = pb.push_link(shared_item.text, shared_item.get_absolute_url())

@receiver(post_save, sender=User)
def create_share_user(sender, instance, created, **kwargs):
    if created:
        ShareUser.objects.create(user=instance)
