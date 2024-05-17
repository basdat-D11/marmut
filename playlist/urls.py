from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    path('', show_playlist, name='show_playlist'),
    path('add_playlist', show_add_playlist, name='add_playlist'),
    path('complete_add_playlist', complete_add_playlist, name='complete_add_playlist'),
    path('detail/<uuid:item_uuid>/', show_detail_playlist, name='detail'),
    path('play', show_play, name='play'),
    path('add_song/<str:item_uuid>/', add_song, name='add_song'),
    path('play_song/<str:item_uuid>/', play_song, name='play_song'),
    path('complete_add_song/<str:item_uuid>/', complete_add_song, name='complete_add_song'),
    path('play_playlist', lihat_detail, name='play_playlist'),
    path('shuffle_play', shuffle, name='shuffle_play'),
    path('playsong', playsong, name='playsong'),
    path('edit_playlist/<str:item_uuid>/', edit_playlist, name='edit_playlist'),
    path('show_edit_playlist/<str:item_uuid>/', show_edit_playlist, name='show_edit_playlist'),
    path('show_add_song/<str:item_uuid>/', show_add_song, name='show_add_song'),
    path('handle_download', handle_download, name='handle_download'),
    path('complete_song_playlist/<str:item_uuid>/', add_song2, name='complete_song_playlist'),
    path('complete/<str:item_uuid>/', add_song2, name='complete'),
    path('delete_playlist', handle_delete_playlist, name='delete_playlist'),
    path('delete_song', handle_delete_song, name='delete_song'),
    ]