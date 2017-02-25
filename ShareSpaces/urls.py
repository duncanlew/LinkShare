"""ShareSpaces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from Spaces.views import *
from ShareUser.views import *
from django.conf.urls.static import static
from django.conf import settings
from Spaces.models import Space

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/spaces', SpaceViewSet)
router.register(r'api/users', UserViewSet)
router.register(r'api/share-users', ShareUserViewSet)
router.register(r'api/shared-items/(?P<space_id>\d+)', SharedItemViewSet, base_name='shareditems')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', login_required(SharedItemListView.as_view()), name='index'),
    url(r'spaces/add/$', login_required(SpacesCreateView.as_view(success_url="/")), name='spaces-add'),
    url(r'spaces/update/(?P<pk>\d+)/$', login_required(SpacesUpdateView.as_view(success_url="/")), name='spaces-update'),
    url(r'space/(?P<space_id>\d+)$', login_required(SharedItemListView.as_view()), name='shared-item-list'),
    url(r'space/(?P<space_id>\d+)/item/(?P<pk>\d+)$', login_required(SharedItemDetailView.as_view()), name='shared-item-detail'),
    url(r'space/(?P<space_id>\d+)/comment/(?P<shareditem_id>\d+)$', login_required(CommentCreateView.as_view()), name='comment-add'),
    url(r'space/(?P<space_id>\d+)/add/$', login_required(SharedItemCreateView.as_view(success_url="/")), name='shareditem-add'),
    url(r'profile$', login_required(ShareUserUpdateView.as_view(success_url="/")), name='shareuser-update'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
