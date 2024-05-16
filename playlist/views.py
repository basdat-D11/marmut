import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, HttpResponseServerError
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from datetime import datetime
import uuid


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
    query_str = f"""SELECT konten.judul as judul, song.id_konten::text as id, akun.nama as oleh, konten.durasi as durasi
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

    print(data_playlist)

    return render(request, 'detail.html', {'playlist': data_playlist, 'lagu': lagu,
                                            'pembuat': pembuat,
                                            'akun': request.session.get('akun', None)})

@csrf_exempt
def lihat_detail(request):
    playlistId = request.POST.get('playlist_id')
    query_str = f"SELECT * FROM user_playlist WHERE id_user_playlist = '{playlistId}'"
    hasil = query(query_str)
    print("hasil adalah " + hasil)
    pembuat = hasil[0]['email_pembuat']
    data_playlist = hasil[0]
    print(playlistId)
    query_str = f"""SELECT konten.judul as judul, song.id_konten::text as id, akun.nama as oleh, konten.durasi as durasi
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

    akun = request.session.get('akun', None)

    return render(request, 'detail_lihat.html', {'playlist': data_playlist, 'lagu': lagu, 'pembuat': pembuat, 'akun': akun})

def show_play(request):
    return render(request, 'play_song.html')


@csrf_exempt
def complete_add_playlist(request):
    if request.method == 'POST':
        nama = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')

    akun = request.session.get('akun', None)
    print(akun['email'])
    uuid1 = str(uuid.uuid4())

    query_str = f"""INSERT INTO marmut.playlist 
    VALUES ('{uuid1}')"""
    query(query_str)

    uuid2 = str(uuid.uuid4())
    tanggal = datetime.now().strftime("%Y-%m-%d")

    query_str = f"""INSERT INTO marmut.user_playlist 
    VALUES ('{akun['email']}', '{uuid2}', '{nama}', '{deskripsi}', '{int(0)}', '{tanggal}', '{uuid1}', '{int(0)}');"""
    a = query(query_str)
    print(a)
    return redirect('playlist:show_playlist')

def add_song(request, item_uuid):
    akun = request.session.get('akun', None)
    email = akun['email']

    query_str = f"SELECT * FROM user_playlist WHERE email_pembuat = '{email}'"
    playlist = query(query_str)

    lagu = item_uuid

    query_str = f"""SELECT konten.judul, akun.nama, konten.id as id FROM song JOIN artist
            ON song.id_artist = artist.id JOIN akun ON
            artist.email_akun = akun.email JOIN konten ON song.id_konten = konten.id
            WHERE song.id_konten = '{lagu}'"""

    
    hasil = query(query_str)
    lagu = hasil[0]

    print(lagu)

    return render(request, 'song_to_playlist.html', {'playlist': playlist, 'lagu': lagu})

def complete_add_song(request, item_uuid):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
    lagu = item_uuid
    query_str = f"""SELECT id_playlist::text FROM user_playlist WHERE id_user_playlist = '{playlist_id}'"""
    hasil = query(query_str)
    hasil = hasil[0]
    playlist_id = hasil['id_playlist']
    query_str = f"""INSERT INTO playlist_song VALUES ('{playlist_id}', '{lagu}')"""
    hasil = query(query_str)
    #cek hasil apakah int
    print(hasil)
    if isinstance(hasil, int):
        query_str = f"""SELECT * FROM user_playlist WHERE id_playlist = '{playlist_id}'"""
        hasil = query(query_str)
        hasil = hasil[0]
        nama_playlist = hasil['judul']

        query_str = f"""SELECT * from song join konten on song.id_konten = konten.id where id_konten = '{lagu}'"""
        hasil = query(query_str)
        hasil = hasil[0]
        nama_lagu = hasil['judul']

        return render(request, 'add_complete.html', {'nama_playlist': nama_playlist, 'nama_lagu': nama_lagu})
    else:
        return render(request, 'error.html')

def download_complete(request):
    return render(request, 'download_complete.html')

def play_song(request, item_uuid):
    query_str = f"""SELECT konten.judul as judul, album.judul as album, konten.id as id, konten.tanggal_rilis as tanggal_rilis,
            konten.tahun as tahun, konten.durasi as durasi, song.total_play as total_play, song.total_download, akun.nama FROM song JOIN artist
            ON song.id_artist = artist.id JOIN akun ON
            artist.email_akun = akun.email JOIN konten ON song.id_konten = konten.id
            JOIN album ON song.id_album = album.id
            WHERE song.id_konten = '{item_uuid}'"""
    hasil = query(query_str)
    lagu = hasil[0]
    artis = []

    query_str = f"""SELECT akun.nama FROM song JOIN artist ON song.id_artist = artist.id 
    JOIN akun ON artist.email_akun = akun.email WHERE song.id_konten = '{item_uuid}'"""
    hasil = query(query_str)

    for a in hasil:
        artis.append(a['nama'])
    

    query_str = f"""SELECT akun.nama from songwriter_write_song JOIN songwriter
    ON songwriter_write_song.id_songwriter = songwriter.id
    JOIN akun ON songwriter.email_akun = akun.email
    WHERE songwriter_write_song.id_song = '{item_uuid}'"""
    hasil = query(query_str)

    songwriter = []
    for s in hasil:
        songwriter.append(s['nama'])

    genre = []

    query_str = f"""SELECT genre.genre FROM song JOIN genre ON song.id_konten = genre.id_konten
    WHERE song.id_konten = '{item_uuid}'"""

    hasil = query(query_str)

    for g in hasil:
        genre.append(g['genre'])

    return render(request, 'play_song.html', {'lagu': lagu, 'artis': artis, 'songwriter': songwriter, 'genre':genre, 'playlist': item_uuid, 'akun': request.session.get('akun', None)})


@csrf_exempt
def edit_playlist(request, item_uuid):
    if request.method == 'POST':
        nama = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')

    query_str = f"""UPDATE user_playlist SET judul = '{nama}', deskripsi = '{deskripsi}' WHERE id_user_playlist = '{item_uuid}'"""
    query(query_str)

    return redirect('playlist:show_playlist')

def show_edit_playlist(request, item_uuid):
    query_str = f"""SELECT judul, deskripsi, id_user_playlist::text FROM user_playlist 
    WHERE id_user_playlist = '{item_uuid}'"""
    hasil = query(query_str)
    hasil = hasil[0]
    print(hasil)
    return render(request, 'edit_playlist.html', {'playlist': hasil})

@csrf_exempt
def playsong(request):
    email = request.session.get('akun', None)['email']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lagu = json.loads(request.body)['lagu']

    query_str = f"""INSERT INTO akun_play_song VALUES ('{email}', '{lagu}', '{time}')"""
    hasil = query(query_str)
    if isinstance(hasil, int):
        print(hasil)
        return HttpResponse('berhasil')
    else:
        return HttpResponseServerError('gagal')
    
 

def shuffle(request):
    idp = json.loads(request.body)['id']
    email = request.session.get('akun', None)['email']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query_str = """SELECT * FROM user_playlist where id_user_playlist = idp """
    hasil = query(query_str)
    hasil = hasil[0]
    id_playlist = hasil['id_playlist']

    query_str = f"""SELECT * from playlist_song where id_playlist='{id_playlist}'"""
    hasil = query(query_str)

    query_str = f"""insert into akun_play_playlist values ('{email}', '{id_playlist}', '{time}')"""
    for a in hasil:
        lagu = hasil['id_song']
        query_str = f"""insert into akun_play_song values ('{email}', '{lagu}', '{time}')"""
        query(query_str)

def show_add_song(request, item_uuid):
    query_str = f"""SELECT konten.judul, konten.id FROM konten join
    song on konten.id = song.id_konten"""
    hasil = query(query_str) 

    query_str = f"""SELECT id_playlist::text FROM user_playlist WHERE id_user_playlist = '{item_uuid}'"""
    playlist = query(query_str)
    playlist = playlist[0]
    return render(request, 'add_song.html', {'lagu': hasil, 'playlist': playlist})


@csrf_exempt
def add_song2(request, item_uuid):
    playlist = item_uuid
    lagu = request.POST.get('lagu')
    query_str = f"""INSERT INTO playlist_song VALUES ('{playlist}', '{lagu}')"""
    hasil = query(query_str)
    if isinstance(hasil, int):
        query_str = f"""SELECT * FROM user_playlist WHERE id_playlist = '{playlist}'"""
        hasil = query(query_str)
        hasil = hasil[0]
        nama_playlist = hasil['judul']

        query_str = f"""SELECT * from song join konten on song.id_konten = konten.id where id_konten = '{lagu}'"""
        hasil = query(query_str)
        hasil = hasil[0]
        nama_lagu = hasil['judul']

        return render(request, 'add_complete.html', {'nama_playlist': nama_playlist, 'nama_lagu': nama_lagu})
    else:
        print(hasil)
        return render(request, 'error.html')

@csrf_exempt
def handle_download(request):
    email = request.session.get('akun', None)['email']
    lagu = json.loads(request.body)['lagu']
    print(lagu)

    query_str = f"""INSERT INTO downloaded_song VALUES ( '{lagu}', '{email}')"""
    hasil = query(query_str)
    if isinstance(hasil, int):
        return HttpResponse('berhasil')
    else:
        print(hasil)
        return HttpResponseServerError('gagal')



"""
show_add_song buat yang pas di playlist pilih songnya add_song.html

add_song2 buat nampilin berhasilnya nanti, rendernya tetep yang add_complete.html

"""