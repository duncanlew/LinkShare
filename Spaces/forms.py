from .models import SharedItem
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

class SharedItemForm(ModelForm):
    class Meta:
        model = SharedItem
        fields = ['url', 'text']
        labels = {
            'url': _('URL'),
            'text': _('Description...'),
        }
