from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def album_create(request):
    query_str = "SELECT nama FROM LABEL"
    result = query(query_str)
    print(result)
    labels = ['Pilih Label'] + [data['nama'] for data in result]
    return render(request, 'album_form.html', {'labels': labels})

def album_list(request):
    query_str = """SELECT a.id, a.judul, l.nama as label, a.jumlah_lagu, a.total_durasi
    FROM album as a
    JOIN label as l ON a.id_label = l.id
    """
    result = query(query_str)

    role = request.session.get('role', None)

    role = "Songwriter"
    if role != "Label":
        return render(request, 'album_list.html', {'albums': result, 'role': role})
    else:
        return render(request, 'album_list_label.html', {'albums': result, 'role': role})

@csrf_exempt
def tambah_lagu(request, id):
    query_str = f"SELECT * from album WHERE id = '{id}'"
    album = query(query_str)
    album['id'] = str(album['id'])

    query_str = """SELECT a.nama
    FROM akun as a
    JOIN artist as s ON a.email = s.email_akun
    """
    results = query(query_str)
    artists = [data['nama'] for data in results]

    query_str = """SELECT a.nama
    FROM akun as a
    JOIN songwriter as s ON a.email = s.email_akun
    """
    results = query(query_str)
    songwriters = [data['nama'] for data in results]

    genres = ['Pop', 'Rock', 'Jazz', 'Hip Hop', 'Electronic', 'R&B', 'Country', 'Classical', 'Reggae']

    role = request.session.get('role', None)

    return render(request, 'lagu_add.html', {
        'album': album,
        'user_logged_in': role,
        'artists': artists,
        'songwriters': songwriters,
        'genres': genres
    })

def daftar_lagu(request, id):
    query_str = f"SELECT judul FROM album WHERE id = '{id}'"
    judul_album = query(query_str)

    query_str = f"""SELECT k.judul, k.durasi, s.total_play, s.total_download
    FROM konten as k
    JOIN song as s ON k.id = s.id_konten
    WHERE id_album = '{id}'
    """
    songs = query(query_str)

    return render(request, 'lagu_list.html', {'album': judul_album, 'songs': songs})