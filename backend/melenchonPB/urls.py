"""melenchonPB URL Configuration

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
import re

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.views.static import serve
from django.utils.http import urlquote

from callcenter.views import CallhubWebhookView
from accounts import urls as accounts_urls
from callcenter import urls as callcenter_urls
from callcenter.actions.callhub import get_webhook_target


def angular_routes(prefix, view=serve, index='index.html', **kwargs):
    """
    Helper function to return a URL pattern for serving the index.html for angular routes in debug mode

    Now serves the index file from document_root, both at the root route, and at every
    route starting with prefix
    """
    if not settings.DEBUG or (prefix and '://' in prefix):
        return []
    elif not prefix:
        raise ImproperlyConfigured("Empty angular prefix not permitted")

    kwargs['path'] = '/%s' % (index,)

    return [
        url(r'^$', view, kwargs=kwargs),
        url(r'^%s' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs)
    ]


urlpatterns = [

    #WEBHOOKS
    url(r'^%s' % get_webhook_target(), CallhubWebhookView.as_view()),

    #Accounts URLs
    url(r'^', include(accounts_urls, namespace='accounts')),

    #API URLs
    url(r'^api/', include(callcenter_urls, namespace='callcenter')),

    #AUTRES URLS
    url(r'^admin/', admin.site.urls),
] + angular_routes(settings.ANGULAR_URL, document_root=settings.ANGULAR_ROOT)
