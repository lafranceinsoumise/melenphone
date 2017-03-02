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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from callcenter import views
from callcenter.views import SampleView, AngularApp, NgTemplateView

ngurls = [
    url(r'^$', SampleView.as_view(), name='sample'),
    url(r'^ng/$', NgTemplateView.as_view(), name='ngTemplate'),
]

urlpatterns = [
    # TEST URL
    url(r'^test/', views.test, name="test"),

    #URL AUTH
    url(r'^registerNew/', views.registerNew, name="register"),
    url(r'^registerSucess/', views.registerSucess, name="register_sucess"),
    url(r'^login/$', auth_views.login, name="login"),
	url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name="logout"),

    #WEBHOOKS
    url(r'^notewebhook/$', views.noteWebhook),

    #API
    url(r'^api/test_websocket/$', views.api_test_socket),

    #AUTRES URLS
    url(r'^admin/', admin.site.urls),
    url(r'^sample/', include(ngurls)),
    url(r'^(?!ng/).*$', AngularApp.as_view(), name="angular_app"),
	url(r'^ng\/$', AngularApp.as_view(), name="angular_app_with_slash"),
] + static(settings.ANGULAR_URL, document_root=settings.ANGULAR_ROOT) + [
] 
