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

from callcenter.views import AngularApp
from callcenter.views import api_user_achievements, api_test_simulatecall, api_leaderboard, api_basic_information, api_test_socket, UserAPI
from callcenter.views import webhook_note
from accounts import urls as accounts_urls


urlpatterns = [

    #WEBHOOKS
    url(r'^webhook/note', webhook_note.as_view()),

    # accounts urls
    url(r'^', include(accounts_urls, namespace='accounts')),

        #API - NO TOKEN REQUIRED
    url(r'^api/test_websocket$', api_test_socket.as_view()),
    url(r'^api/simulate_call$', api_test_simulatecall.as_view()),
    url(r'^api/basic_information$', api_basic_information.as_view()),
    url(r'^api/leaderboard/(?P<ranking>\w{0,10})$', api_leaderboard.as_view()),
        #API - TOKEN REQUIRED
    url(r'^api/current_user/profile$', UserAPI.as_view()),
    url(r'^api/current_user/achievements$', api_user_achievements.as_view()),

    #REST_FRAMEWORK

    #AUTRES URLS
    url(r'^admin', admin.site.urls),

    #ANGULAR
    url(r'^(?!ng/).*$', AngularApp.as_view(), name="angular_app"),
    url(r'^ng/pokechon$', AngularApp.as_view(), name="angular_app"),
    url(r'^ng/login$', AngularApp.as_view(), name="angular_app"),
    url(r'^ng/register$', AngularApp.as_view(), name="angular_app"),
	url(r'^ng/$', AngularApp.as_view(), name="angular_app"),
] + static(settings.ANGULAR_URL, document_root=settings.ANGULAR_ROOT)
