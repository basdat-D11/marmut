from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

def lihat_chart(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT tipe FROM marmut.chart")  # Pastikan skema yang benar
        charts = cursor.fetchall()
    
    context = {
        'charts': [{'tipe': row[0]} for row in charts]
    }

    return render(request, 'lihat_chart.html', context)

def detail_chart(request):
    tipe_top = request.GET.get('tipe_top')
    with connection.cursor() as cursor:
        if tipe_top == "Daily Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", artist.email_akun AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM marmut.akun_play_song
                JOIN marmut.song ON akun_play_song.id_song = song.id_konten 
                JOIN marmut.konten ON song.id_konten = konten.id 
                JOIN marmut.artist ON song.id_artist = artist.id 
                WHERE akun_play_song.waktu::date = CURRENT_DATE
                GROUP BY konten.id, konten.judul, artist.email_akun, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        elif tipe_top == "Weekly Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", artist.email_akun AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM marmut.akun_play_song
                JOIN marmut.song ON akun_play_song.id_song = song.id_konten 
                JOIN marmut.konten ON song.id_konten = konten.id 
                JOIN marmut.artist ON song.id_artist = artist.id 
                WHERE akun_play_song.waktu >= date_trunc('week', CURRENT_DATE)
                GROUP BY konten.id, konten.judul, artist.email_akun, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        elif tipe_top == "Monthly Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", artist.email_akun AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM marmut.akun_play_song
                JOIN marmut.song ON akun_play_song.id_song = song.id_konten 
                JOIN marmut.konten ON song.id_konten = konten.id 
                JOIN marmut.artist ON song.id_artist = artist.id 
                WHERE akun_play_song.waktu >= date_trunc('month', CURRENT_DATE)
                GROUP BY konten.id, konten.judul, artist.email_akun, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        elif tipe_top == "Yearly Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", artist.email_akun AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM marmut.akun_play_song
                JOIN marmut.song ON akun_play_song.id_song = song.id_konten 
                JOIN marmut.konten ON song.id_konten = konten.id 
                JOIN marmut.artist ON song.id_artist = artist.id 
                WHERE akun_play_song.waktu >= date_trunc('year', CURRENT_DATE)
                GROUP BY konten.id, konten.judul, artist.email_akun, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid chart type'})
        song_favorit = cursor.fetchall()
    
    songs = [
        {
            'id_lagu': row[0], 
            'title': row[1], 
            'artist': row[2], 
            'release_date': row[3].strftime('%d/%m/%Y'), 
            'total_plays': row[4]
        } for row in song_favorit]
    
    return JsonResponse({'status': 'success', 'songs': songs})
