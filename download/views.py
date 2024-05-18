from django.shortcuts import redirect, render
from utils.query import query

# Create your views here.
def downloaded_songs(request):
    akun = request.session.get('akun', None)

    role = akun['role']

    if akun['premium'] == True:
        email = akun['email']

        query_str = f"""
        SELECT k.judul AS title, a.nama AS artist, s.id_konten AS id
        FROM marmut.downloaded_song ds
        JOIN marmut.song s ON ds.id_song = s.id_konten
        JOIN marmut.artist ar ON s.id_artist = ar.id
        JOIN marmut.akun a ON ar.email_akun = a.email
        JOIN marmut.konten k ON s.id_konten = k.id
        WHERE ds.email_downloader = '{email}';
        """

        songs = query(query_str)
        
        return render(request, 'downloaded_songs.html', {'songs': songs, 'premium': True, 'role': role})
    else:
        return render(request, 'downloaded_songs.html', {'premium': False, 'role': role})

def song_deleted(request, song_title):
    akun = request.session.get('akun', None)

    role = akun['role']
    premium = akun['premium']

    query_str = f"""
    DELETE FROM marmut.downloaded_song
    USING marmut.konten
    WHERE marmut.downloaded_song.id_song = marmut.konten.id
    AND marmut.konten.judul = '{song_title}';
    """

    query(query_str)

    return render(request, 'song_deleted.html', {'song_title': song_title, 'role': role, 'premium': premium})