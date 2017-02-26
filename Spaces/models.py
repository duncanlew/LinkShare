from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from ShareUser.models import *
from ShareSpaces.settings import ALLOWED_HOSTS
import re
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .image_helpers import get_page_text, get_image_size
import urllib.request
import os
from django.core.files import File
from django.core.files.base import ContentFile
import newspaper
from newspaper import Article
import requests
from PIL import Image
from io import BytesIO
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
    image_file = models.ImageField(upload_to='images', null=True)
    image_url = models.URLField(null=True)

    def save(self, *args, **kwargs):
        self.get_newspaper_info()
        self.get_remote_image()
        super(SharedItem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        host = 'localhost' if len(ALLOWED_HOSTS) is 0 else ALLOWED_HOSTS[0]
        return 'https://{0}{1}'.format(host, reverse('shared-item-detail', kwargs={'space_id': self.space.id, 'pk': self.pk}))

    def get_newspaper_info(self):
        article = Article(self.url)
        article.download()
        article.parse()

        if not self.text:
            self.text = article.title
        self.image_url = article.top_image

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            img_data = requests.get(self.image_url).content
            pil_image = Image.open(BytesIO(img_data))
            self.image_file.save(
                os.path.basename(self.image_url),
                content=ContentFile(img_data)
            )


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(to=ShareUser)
    created = models.DateTimeField(auto_now_add=True)
    shared_item = models.ForeignKey(to=SharedItem)

    def get_absolute_url(self):
        return self.shared_item.get_absolute_url()

@receiver(post_save, sender=Comment)
@receiver(post_save, sender=SharedItem)
def send_notification_to_all(sender, instance, created, **kwargs):
    if sender.__name__ is 'SharedItem':
        user_list = instance.space.added_users.all()
    if sender.__name__ is 'Comment':
        instance.text = '{0} says: {1}'.format(instance.user, instance.text)
        user_list = instance.shared_item.space.added_users.all()
    for s_user in user_list:
        s_user.send_notification(instance)
