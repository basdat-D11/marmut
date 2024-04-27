import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


def show_playlist(request):
    akun = request.session.get('akun', None)
    email = akun['email']
    query_str = f"SELECT * FROM user_playlist WHERE email_pembuat = '{email}'"
    hasil = query(query_str)
    return render(request, 'playlist.html', {'playlist': hasil})

def show_add_playlist(request):
    return render(request, 'add_playlist.html')

@csrf_exempt
def show_detail_playlist(request):
    playlistId = request.POST.get('playlist_id')
    query_str = f"SELECT * FROM user_playlist WHERE id_user_playlist = '{playlistId}'"
    hasil = query(query_str)
    pembuat = hasil[0]['email_pembuat']
    data_playlist = hasil[0]
    print(playlistId)
    query_str = f"""SELECT konten.judul as judul, akun.nama as oleh, konten.durasi as durasi
    FROM playlist_song JOIN konten ON playlist_song.id_song = konten.id 
    JOIN user_playlist ON playlist_song.id_playlist = user_playlist.id_playlist
    JOIN song ON konten.id = song.id_konten
    JOIN artist ON song.id_artist = artist.id 
    JOIN akun ON artist.email_akun = akun.email
    WHERE id_user_playlist = '{playlistId}'"""

    hasil = query(query_str)
    lagu = hasil
    print(hasil)

    query_str = f"SELECT * FROM akun WHERE email = '{pembuat}'"
    hasil = query(query_str)
    pembuat = hasil[0]['nama']

    return render(request, 'detail.html', {'playlist': data_playlist, 'lagu': lagu, 'pembuat': pembuat})

def show_play(request):
    return render(request, 'play_song.html')