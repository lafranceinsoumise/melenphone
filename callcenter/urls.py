from django.conf.urls import url, include

from . import views

urlpatterns = [
    # API - NO AUTH REQUIRED
    url(r'^test_websocket$', views.api_test_socket.as_view()),
    url(r'^simulate_call$', views.api_test_simulatecall.as_view()),
    url(r'^basic_information$', views.api_basic_information.as_view()),
    url(r'^leaderboard/(?P<ranking>\w{0,10})$', views.api_leaderboard.as_view()),
    # API - AUTH REQUIRED
    url(r'^current_user/profile$', views.UserAPI.as_view()),
    url(r'^current_user/caller_information$', views.CallerInformationAPI.as_view()),
    url(r'^current_user/achievements$', views.api_user_achievements.as_view()),
]
