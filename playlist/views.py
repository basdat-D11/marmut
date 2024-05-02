import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from datetime import datetime


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

@csrf_exempt
def lihat_detail(request):
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

    return render(request, 'detail_lihat.html', {'playlist': data_playlist, 'lagu': lagu, 'pembuat': pembuat})

def show_play(request):
    return render(request, 'play_song.html')

def add_playlist(request):
    data = json.loads(request.body)

    nama = data['nama']
    deskripsi = data['deskripsi']

    akun = request.session.get('akun', None)
    uuid = str(uuid.uuid4())

    query_str = f"""INSERT INTO palylist (id) VALUES ('{uuid}')"""
    query(query_str)

    uuid2 = str(uuid.uuid4())
    tanggal = datetime.now().strftime("%Y-%m-%d")

    query_str = f"""INSERT INTO marmut.user_playlist VALUES ('{akun['email']}', '{uuid2}', '{nama}', '{deskripsi}', 0, '{tanggal}', '{uuid}', 0);"""
    query(query_str)

    return JsonResponse({'status': 'success'})

def add_song(request):
    return render(request, 'song_to_playlist.html')

def complete_add_song(request):
    return render(request, 'add_complete.html')

def download_complete(request):
    return render(request, 'download_complete.html')