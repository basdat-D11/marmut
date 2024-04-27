from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    path('', show_playlist, name='show_playlist'),
    path('add_playlist', show_add_playlist, name='add_playlist'),
    path('detail', show_detail_playlist, name='detail'),
    path('play', show_play, name='play'),
    ]