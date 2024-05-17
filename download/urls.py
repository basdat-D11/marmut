from django.urls import path
from download.views import *

app_name = 'download'

urlpatterns = [
    path('', downloaded_songs, name='downloaded_songs'),
    path('song_deleted/<str:song_title>/', song_deleted, name='song_deleted'),
]