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
from django.conf.urls import url
from django.contrib import admin
from callcenter import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^agent_key/', views.agent_key),
    url(r'^agent_status/', views.agent_status),
    url(r'^set_webhook/', views.set_webhook),
    url(r'^get_webhook/', views.get_webhook),
    url(r'^campaign_info/', views.campaign_info),
    url(r'^campaign_info/', views.campaign_info),
    url(r'^is_trophy/', views.is_trophy),
]
