from django.urls import path
from .views import spotify_login, spotify_callback, create_playlist

urlpatterns = [
    path('login/', spotify_login, name='spotify-login'),
    path('callback/', spotify_callback, name='spotify-callback'),
    path('create/', create_playlist, name='create-playlist'),
]