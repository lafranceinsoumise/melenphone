from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    # API - NO AUTH REQUIRED
    url(r'^basic_information$', views.BasicInformationView.as_view()),
    url(r'^leaderboard$', views.LeaderboardsView.as_view()),
    # API - AUTH REQUIRED
    url(r'^current_user/profile$', views.UserView.as_view()),
    url(r'^current_user/caller_information$', views.CallerInformationView.as_view()),
    url(r'^current_user/associate_existing_agent$', views.AssociateExistingCallerAgentView.as_view()),
    url(r'^current_user/achievements$', views.UserAchievementsView.as_view()),
]

if settings.DEBUG == True:
    urlpatterns += [
    url(r'^test_websocket$', views.TestSocketView.as_view()),
    url(r'^simulate_call$', views.SimulateCallView.as_view()),
    url(r'^simulate_achievement$', views.SimulateAchievementView.as_view())
    ]