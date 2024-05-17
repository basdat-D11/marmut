from datetime import datetime
import uuid
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def album_create(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        id_label = request.POST.get('label')
        print(judul)
        print(id_label)
        id_album = str(uuid.uuid4())
        query_str = f"""INSERT INTO album (id, judul, jumlah_lagu, id_label, total_durasi)
            VALUES (
                '{id_album}',
                '{judul}',
                0,
                '{id_label}',
                0
            )
            """
        res = query(query_str)
        print(res)

        judul = request.POST.get('judul')
        artist_email = request.POST.get('artist_email')
        songwriters_email = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')
        
        print(artist_email)

        id_konten = str(uuid.uuid4())
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        tahun = current_date.strftime('%Y')

        #Buat konten
        query_str = f"""INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi)
        VALUES (
            '{id_konten}',
            '{judul}',
            '{formatted_date}',
            {tahun},
            {durasi}
        )
        """
        print(query(query_str))

        #Buat relasi song
        id_artist = query(f"SELECT id FROM artist WHERE email_akun = '{artist_email}'")[0]['id']
        query_str = f"""INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download)
        VALUES (
            '{id_konten}',
            '{id_artist}',
            '{id_album}',
            0,
            0
        )
        """
        print(query(query_str))

        #Tambahin semua genre ke song
        for genre in genres:
            query_str = f"""INSERT INTO genre (id_konten, genre)
            VALUES (
                '{id_konten}',
                '{genre}'
            )
            """
            print(query(query_str))

        #Tambah songwriter_write_song utk semua songwriter
        songwriters = query("SELECT id, email_akun FROM songwriter")
        songwriters_id = [songwriter['id'] for songwriter in songwriters if songwriter['email_akun'] in songwriters_email]

        for songwriter_id in songwriters_id:
            query_str = f"""INSERT INTO songwriter_write_song (id_songwriter, id_song)
            VALUES (
                '{songwriter_id}',
                '{id_konten}'
            )
            """
            print(query(query_str))


        print(songwriters_email)

        #Ga perlu update durasi sm jumlah lagu di album gausah soalnya pake trigger

        return redirect('album:album_list')

    query_str = """SELECT a.nama, a.email
    FROM akun as a
    JOIN artist as s ON a.email = s.email_akun
    """
    artists = query(query_str)

    query_str = """SELECT a.nama, a.email
    FROM akun as a
    JOIN songwriter as s ON a.email = s.email_akun
    """
    songwriters = query(query_str)
    print(songwriters)

    genres = ['Pop', 'Rock', 'Jazz', 'Hip Hop', 'Electronic', 'R&B', 'Country', 'Classical', 'Reggae']

    akun = request.session.get('akun', None)
    nama_akun = akun['nama'] if akun else ''


    query_str = "SELECT nama, id FROM LABEL"
    labels = query(query_str)


    return render(request, 'album_form.html', {
        'labels': labels,
        'role': akun['role'],
        'name': nama_akun,
        'email': akun['email'],
        'artists': artists,
        'songwriters': songwriters,
        'genres': genres
    })

def album_list(request):
    query_str = """SELECT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi
    FROM album as a
    JOIN label as l ON a.id_label = l.id
    """
    result = query(query_str)

    akun = request.session.get('akun', None)
    print(akun)
    role = ''
    role = "Label" if akun and not akun.get('role', None) else "Bukan Label"

    data = {'albums': result, 'role': role}
    data.update(akun)

    if role != "Label":
        return render(request, 'album_list.html', data)
    else:
        return render(request, 'album_list_label.html', data)

@csrf_exempt
def tambah_lagu(request, id):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        artist_email = request.POST.get('artist_email')
        songwriters_email = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')
        
        print(artist_email)

        id_konten = str(uuid.uuid4())
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        tahun = current_date.strftime('%Y')

        #Buat konten
        query_str = f"""INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi)
        VALUES (
            '{id_konten}',
            '{judul}',
            '{formatted_date}',
            {tahun},
            {durasi}
        )
        """
        print(query(query_str))

        #Buat relasi song
        id_artist = query(f"SELECT id FROM artist WHERE email_akun = '{artist_email}'")[0]['id']
        query_str = f"""INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download)
        VALUES (
            '{id_konten}',
            '{id_artist}',
            '{id}',
            0,
            0
        )
        """
        print(query(query_str))

        #Tambahin semua genre ke song
        for genre in genres:
            query_str = f"""INSERT INTO genre (id_konten, genre)
            VALUES (
                '{id_konten}',
                '{genre}'
            )
            """
            print(query(query_str))

        #Tambah songwriter_write_song utk semua songwriter
        songwriters = query("SELECT id, email_akun FROM songwriter")
        songwriters_id = [songwriter['id'] for songwriter in songwriters if songwriter['email_akun'] in songwriters_email]

        for songwriter_id in songwriters_id:
            query_str = f"""INSERT INTO songwriter_write_song (id_songwriter, id_song)
            VALUES (
                '{songwriter_id}',
                '{id_konten}'
            )
            """
            print(query(query_str))


        print(songwriters_email)

        #Ga perlu update durasi sm jumlah lagu di album gausah soalnya pake trigger

        return redirect('album:album_list')
    elif 'role' not in request.session.get('akun', {}):
        return redirect('album:album_list')
    else:
        query_str = f"SELECT * from album WHERE id = '{id}'"
        album = query(query_str)[0]
        album['id'] = str(album['id'])
        print(album)

        query_str = """SELECT a.nama, a.email
        FROM akun as a
        JOIN artist as s ON a.email = s.email_akun
        """
        artists = query(query_str)

        query_str = """SELECT a.nama, a.email
        FROM akun as a
        JOIN songwriter as s ON a.email = s.email_akun
        """
        songwriters = query(query_str)
        print(songwriters)

        genres = ['Pop', 'Rock', 'Jazz', 'Hip Hop', 'Electronic', 'R&B', 'Country', 'Classical', 'Reggae']

        akun = request.session.get('akun', None)
        nama_akun = akun['nama'] if akun else ''

        return render(request, 'lagu_add.html', {
            'album': album,
            'role': akun['role'],
            'name': nama_akun,
            'email': akun['email'],
            'artists': artists,
            'songwriters': songwriters,
            'genres': genres
        })

def daftar_lagu(request, id):
    query_str = f"SELECT judul FROM album WHERE id = '{id}'"
    judul_album = query(query_str)

    query_str = f"""SELECT k.judul, k.durasi, s.total_play, s.total_download, k.id
    FROM konten as k
    JOIN song as s ON k.id = s.id_konten
    WHERE id_album = '{id}'
    """
    songs = query(query_str)

    return render(request, 'lagu_list.html', {'album': judul_album, 'songs': songs})

@csrf_exempt
def delete_album(request, id):
    if request.method == 'POST':
        query(f"DELETE FROM album WHERE id = '{id}'")
        return JsonResponse({'status': 'success'})
    return HttpResponseNotFound()

@csrf_exempt
def delete_lagu(request, id):
    if request.method == 'POST':
        status = True
        res = query(f"DELETE FROM genre WHERE id_konten = '{id}'")
        status = status and isinstance(res, int)
        res = query(f"DELETE FROM songwriter_write_song WHERE id_song = '{id}'")
        status = status and isinstance(res, int)
        res = query(f"DELETE FROM song WHERE id_konten = '{id}'")
        status = status and isinstance(res, int)
        res = query(f"DELETE FROM konten WHERE id = '{id}'")
        status = status and isinstance(res, int)
        if res:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'})
    return HttpResponseNotFound()