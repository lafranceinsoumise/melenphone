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
from callcenter.views import AngularApp
from callcenter.views import api_user_infos, api_user_achievements, api_test_simulatecall, api_leaderboard, api_basic_information, api_user
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    #WEBHOOKS
    url(r'^notewebhook$', views.noteWebhook),

    #API
        #TOKEN
    url(r'^api/token/auth', obtain_jwt_token),
    url(r'^api/token/refresh', refresh_jwt_token),
        #API - NO TOKEN REQUIRED
    url(r'^api/test_websocket$', views.api_test_socket.as_view()),
    url(r'^api/simulate_call$', views.api_test_simulatecall.as_view()),
    url(r'^api/basic_information$', views.api_basic_information.as_view()),
    url(r'^api/leaderboard/(?P<ranking>\w{0,10})$', views.api_leaderboard.as_view()),
        #API - TOKEN REQUIRED
    url(r'^api/user/infos$', api_user_infos.as_view()),
    url(r'^api/user/achievements$', api_user_achievements.as_view()),

    #REST_FRAMEWORK
    url(r'^api/user/$', api_user.as_view()),

    #AUTRES URLS
    url(r'^admin/', admin.site.urls),

    #ANGULAR
    url(r'^(?!ng/).*$', AngularApp.as_view(), name="angular_app"),
    url(r'^ng/pokechon$', AngularApp.as_view(), name="angular_app"),
    url(r'^ng/login$', AngularApp.as_view(), name="angular_app"),
    url(r'^ng/registration$', AngularApp.as_view(), name="angular_app"),
	url(r'^ng/$', AngularApp.as_view(), name="angular_app"),
] + static(settings.ANGULAR_URL, document_root=settings.ANGULAR_ROOT)
