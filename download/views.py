from django.shortcuts import render

# Create your views here.
def downloaded_songs(request):
    # Data lagu statis yang akan ditampilkan di tabel
    songs = [
        {'title': 'Song1', 'artist': 'Artist1', 'download_date': '20/02/2024'},
        {'title': 'Song2', 'artist': 'Artist2', 'download_date': '21/03/2024'},
    ]
    
    # Render template dengan data lagu yang diberikan
    return render(request, 'downloaded_songs.html', {'songs': songs})

def song_deleted(request, song_title):
    # Render halaman konfirmasi penghapusan dengan judul lagu
    return render(request, 'song_deleted.html', {'song_title': song_title})