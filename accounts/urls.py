from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^connexion/$', views.RedirectToAuthProvider.as_view(), name='connexion'),
    url(r'^connexion/retour$', views.AuthReturn.as_view(), name='oauth_callback'),
    url(r'^deconnexion/$', logout, {'next_page': 'index'}, name='deconnexion')
]
