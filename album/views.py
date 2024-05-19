from datetime import datetime
import uuid
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def album_create(request):
    if request.method == 'POST':
        judul = request.POST.get('judul_album')
        id_label = request.POST.get('label')
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

        judul = request.POST.get('judul')
        artist_email = request.POST.get('artist_email')
        songwriters_email = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')

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

        #Tambahin royalti
        list_pemilik_hak_cipta = []
        list_pemilik_hak_cipta += query(f"SELECT id_pemilik_hak_cipta FROM artist WHERE id = '{id_artist}'")
        list_pemilik_hak_cipta += query(f"SELECT id_pemilik_hak_cipta FROM songwriter WHERE id in {tuple(songwriters_id)}")
        list_pemilik_hak_cipta += query(f"SELECT l.id_pemilik_hak_cipta FROM label l JOIN album a ON a.id_label = l.id WHERE a.id = '{id_album}'")
        ids_pemilik_hak_cipta = [pemilik['id_pemilik_hak_cipta'] for pemilik in list_pemilik_hak_cipta]

        for ids in ids_pemilik_hak_cipta:
            print(query(f"INSERT INTO royalti VALUES('{ids}', '{id_konten}', 0)"))

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

    data = {
        'labels': labels,
        'role': akun['role'],
        'name': nama_akun,
        'email': akun['email'],
        'artists': artists,
        'songwriters': songwriters,
        'genres': genres
    }
    data.update(akun)

    return render(request, 'album_form.html', data)

def album_list(request):
    if not request.session.get('akun', None):
        return redirect('main:dashboard')
    akun = request.session.get('akun')
    role = akun.get('role', 'podcaster')
    if role == 'podcaster':
        return redirect('main:dashboard')

    if role != "label":
        query_str = f"""
        SELECT A.judul, L.nama AS label, A.jumlah_lagu, A.total_durasi, A.id
        FROM ALBUM A
        JOIN LABEL L ON A.id_label = L.id
        JOIN SONG S ON A.id = S.id_album
        JOIN ARTIST Ar ON S.id_artist = Ar.id
        JOIN AKUN Ak ON Ar.email_akun = Ak.email
        WHERE Ak.email = '{akun['email']}'

        UNION

        SELECT A.judul, L.nama AS label, A.jumlah_lagu, A.total_durasi, A.id
        FROM ALBUM A
        JOIN LABEL L ON A.id_label = L.id
        JOIN SONG S ON A.id = S.id_album
        JOIN SONGWRITER_WRITE_SONG SW ON S.id_konten = SW.id_song
        JOIN SONGWRITER So ON SW.id_songwriter = So.id
        JOIN AKUN Ak ON So.email_akun = Ak.email
        WHERE Ak.email = '{akun['email']}'

        ORDER BY judul ASC;
        """
    else:
        query_str = f"""SELECT A.judul, L.nama AS label, A.jumlah_lagu, A.total_durasi, A.id
            FROM ALBUM A, LABEL L
            WHERE A.id_label = L.id AND L.email = '{akun['email']}'
            ORDER BY A.judul ASC"""
    result = query(query_str)
    print(result)

    data = {'albums': result}
    data.update(akun)

    if role != "label":
        return render(request, 'album_list.html', data)
    else:
        return render(request, 'album_list_label.html', data)

@csrf_exempt
def tambah_lagu(request, id):
    akun = request.session.get('akun', None)
    if not akun:
        return redirect('main:page_login')
    role = akun.get('role', 'bukan_siapa_siapa')
    print(role)
    print(akun)
    if not (role == 'artis' or role == 'songwriter'):
        return redirect('main:dashboard')
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
        songwriters_id = [str(sw['id']) for sw in songwriters if sw['email_akun'] in songwriters_email]

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

        #Tambahin royalti
        list_pemilik_hak_cipta = []
        list_pemilik_hak_cipta += query(f"SELECT id_pemilik_hak_cipta FROM artist WHERE id = '{id_artist}'")
        list_pemilik_hak_cipta += query(f"SELECT id_pemilik_hak_cipta FROM songwriter WHERE id in {tuple(songwriters_id)}")
        list_pemilik_hak_cipta += query(f"SELECT l.id_pemilik_hak_cipta FROM label l JOIN album a ON a.id_label = l.id WHERE a.id = '{id}'")
        print(list_pemilik_hak_cipta)
        ids_pemilik_hak_cipta = [pemilik['id_pemilik_hak_cipta'] for pemilik in list_pemilik_hak_cipta]

        for ids in ids_pemilik_hak_cipta:
            print(query(f"INSERT INTO royalti VALUES('{ids}', '{id_konten}', 0)"))

        return redirect('album:album_list')
    elif 'role' not in request.session.get('akun', {}):
        return redirect('album:album_list')
    else:
        query_str = f"SELECT * from album WHERE id = '{id}'"
        album = query(query_str)[0]
        album['id'] = str(album['id'])

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

        data = {
            'album': album,
            'role': akun['role'],
            'name': nama_akun,
            'email': akun['email'],
            'artists': artists,
            'songwriters': songwriters,
            'genres': genres
        }
        data.update(akun)

        return render(request, 'lagu_add.html', data)

def daftar_lagu(request, id):
    akun = request.session.get('akun', None)
    if not akun:
        return redirect('main:page_login')
    role = akun.get('role', 'podcaster')
    if role == 'podcaster':
        return redirect('main:dashboard')
    
    #Asumsi yang ditampilkan adalah seluruh lagu pada album yg terkait bukan hanya milik artis/songwriter/labelnya

    query_str = f"SELECT judul FROM album WHERE id = '{id}'"
    judul_album = query(query_str)

    query_str = f"""SELECT k.judul, k.durasi, s.total_play, s.total_download, k.id
    FROM konten as k
    JOIN song as s ON k.id = s.id_konten
    WHERE id_album = '{id}'
    """
    songs = query(query_str)

    data = {'album': judul_album, 'songs': songs}
    data.update(request.session.get('akun', None))

    return render(request, 'lagu_list.html', data)

@csrf_exempt
def delete_album(request, id):
    akun = request.session.get('akun', None)
    if not akun:
        return redirect('main:page_login')
    role = akun.get('role', 'podcaster')
    if role == 'podcaster':
        return redirect('main:dashboard')
    
    if request.method == 'POST':
        songs = query(f"SELECT id_konten FROM song WHERE id_album = '{id}'")
        print(songs)
        for ids in songs:
            delete_song(ids['id_konten'])

        s = query(f"DELETE FROM album WHERE id = '{id}'")
        print(s)
        return JsonResponse({'status': 'success'})
    return HttpResponseNotFound()

@csrf_exempt
def delete_lagu(request, id):
    akun = request.session.get('akun', None)
    if not akun:
        return redirect('main:page_login')
    role = akun.get('role', 'podcaster')
    if role == 'podcaster':
        return redirect('main:dashboard')

    if request.method == 'POST':
        status = delete_song(id)
        if status:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'})
    return HttpResponseNotFound()

def delete_song(id):
    status = True
    res = query(f"DELETE FROM genre WHERE id_konten = '{id}'")
    status = status and isinstance(res, int)
    res = query(f"DELETE FROM songwriter_write_song WHERE id_song = '{id}'")
    status = status and isinstance(res, int)
    res = query(f"DELETE FROM song WHERE id_konten = '{id}'")
    status = status and isinstance(res, int)
    res = query(f"DELETE FROM konten WHERE id = '{id}'")
    status = status and isinstance(res, int)
    return status