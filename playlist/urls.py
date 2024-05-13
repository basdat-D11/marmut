from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    path('', show_playlist, name='show_playlist'),
    path('add_playlist', show_add_playlist, name='add_playlist'),
    path('detail', show_detail_playlist, name='detail'),
    path('play', show_play, name='play'),
    path('add_song', add_song, name='add_song'),
    path('complete_add_song', complete_add_song, name='complete_add_song'),
    path('play_playlist', lihat_detail, name='play_playlist'),
    ]