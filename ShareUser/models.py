from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from pushbullet import Pushbullet

# Create your models here.

class ShareUser(models.Model):
    pushbullet_api_key = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(to=User)
    icon = models.ImageField(upload_to='user_icons/',  default = 'user_icons/user_icon.jpg')

    def send_notification(self, item):
        pb = Pushbullet(self.pushbullet_api_key)
        push = pb.push_link(item.text, item.get_absolute_url())

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_share_user(sender, instance, created, **kwargs):
    if created:
        ShareUser.objects.create(user=instance)
