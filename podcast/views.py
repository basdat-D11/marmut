import json
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import uuid
import logging
import psycopg2

logger = logging.getLogger(__name__)

def kelola_podcast(request):
    akun = request.session.get('akun')
    if not akun:
        return redirect('login')

    premium = request.session.get('premium', False)
    role = akun['role']
    context = {
        'akun': akun,
        'premium': premium,
        'role': role,
    }
    return render(request, 'kelolapodcast.html', context)

@csrf_exempt
def create_podcast(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            judul = data.get('judul')
            genres = data.get('genre')
            email_podcaster = request.session.get('akun')['email']
            konten_id = str(uuid.uuid4())
            tanggal_rilis = datetime.now().strftime("%Y-%m-%d")
            tahun_rilis = datetime.now().year

            query_str = f"""
            INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi)
            VALUES ('{konten_id}', '{judul}', '{tanggal_rilis}', '{tahun_rilis}', 0);
            """
            query(query_str)
            logger.info(f"Inserted into konten: {konten_id}, {judul}")

            query_str = f"""
            INSERT INTO podcast (id_konten, email_podcaster)
            VALUES ('{konten_id}', '{email_podcaster}');
            """
            query(query_str)
            logger.info(f"Inserted into podcast: {konten_id}, {email_podcaster}")

            for genre in genres:
                query_str = f"INSERT INTO genre (id_konten, genre) VALUES ('{konten_id}', '{genre}');"
                query(query_str)
                logger.info(f"Inserted into genre: {konten_id}, {genre}")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error inserting podcast: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return render(request, 'createpodcast.html')

def list_podcast(request):
    akun = request.session.get('akun')
    if not akun:
        return redirect('login')

    email_podcaster = akun['email']
    query_str = f"""
    SELECT podcast.id_konten, konten.judul, COUNT(episode.id_episode) as jumlah_episode, COALESCE(SUM(episode.durasi), 0) as total_durasi
    FROM podcast 
    LEFT JOIN konten ON podcast.id_konten = konten.id 
    LEFT JOIN episode ON podcast.id_konten = episode.id_konten_podcast 
    WHERE podcast.email_podcaster = '{email_podcaster}' 
    GROUP BY podcast.id_konten, konten.judul;
    """
    hasil = query(query_str)
    logger.info(f"Fetched podcasts for {email_podcaster}: {hasil}")
    return render(request, 'listpodcast.html', {'podcasts': hasil})

@csrf_exempt
def create_episode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            podcast_id = data.get('podcast')
            judul = data.get('judul')
            deskripsi = data.get('deskripsi')
            durasi = data.get('durasi')
            episode_id = str(uuid.uuid4())
            tanggal_rilis = datetime.now().strftime("%Y-%m-%d")

            durasi_menit = 0
            try:
                if 'jam' in durasi.lower():
                    hours, minutes = durasi.lower().split('jam')
                    durasi_menit += int(hours.strip()) * 60
                    if 'menit' in minutes:
                        minutes = minutes.split('menit')[0]
                        durasi_menit += int(minutes.strip())
                elif 'menit' in durasi.lower():
                    minutes = durasi.lower().split('menit')[0]
                    durasi_menit += int(minutes.strip())
                else:
                    durasi_menit = int(durasi.strip())
            except ValueError:
                logger.error(f"Invalid duration format: {durasi}")
                return JsonResponse({'status': 'error', 'message': 'Invalid duration format'}, status=400)

            query_str = f"""
            INSERT INTO episode (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
            VALUES ('{episode_id}', '{podcast_id}', '{judul}', '{deskripsi}', '{durasi_menit}', '{tanggal_rilis}');
            """
            query(query_str)
            logger.info(f"Inserted into episode: {episode_id}, {judul}")

            query_str = f"""
            UPDATE konten SET durasi = durasi + {durasi_menit} WHERE id = '{podcast_id}';
            """
            query(query_str)
            logger.info(f"Updated total duration in konten: {podcast_id}")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error inserting episode: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    akun = request.session.get('akun')
    if not akun:
        return redirect('login')

    email_podcaster = akun['email']
    query_str = f"SELECT podcast.id_konten, konten.judul FROM podcast JOIN konten ON podcast.id_konten = konten.id WHERE podcast.email_podcaster = '{email_podcaster}';"
    hasil = query(query_str)
    return render(request, 'createepisode.html', {'podcasts': hasil})

def daftar_episode(request):
    podcast_id = request.GET.get('podcast')
    if not podcast_id:
        logger.error("No podcast_id provided")
        return JsonResponse({'status': 'error', 'message': 'No podcast_id provided'}, status=400)

    logger.info(f"Received podcast_id: {podcast_id}")

    query_str = f"SELECT id_konten_podcast, id_episode, judul, deskripsi, durasi, tanggal_rilis FROM episode WHERE id_konten_podcast = '{podcast_id}';"
    hasil = query(query_str)
    logger.info(f"Fetched episodes for podcast {podcast_id}: {hasil}")

    if not isinstance(hasil, list):
        logger.error(f"Query result is not iterable: {hasil}")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

    return render(request, 'daftarepisode.html', {'episodes': hasil})

@csrf_exempt
def play_podcast(request):
    podcast_id = request.GET.get('podcast_id')
    data_podcast = {}
    data_episode = []

    # Query to get podcast details
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT konten.judul, konten.tanggal_rilis, konten.tahun, AKUN.nama AS podcaster_name, SUM(episode.durasi) AS total_durasi
            FROM marmut.podcast
            JOIN marmut.podcaster ON podcast.email_podcaster = podcaster.email 
            JOIN marmut.AKUN ON podcaster.email = AKUN.email 
            JOIN marmut.konten ON podcast.id_konten = konten.id 
            JOIN marmut.episode ON podcast.id_konten = episode.id_konten_podcast
            WHERE marmut.podcast.id_konten = %s
            GROUP BY konten.judul, konten.tanggal_rilis, konten.tahun, AKUN.nama;
        """, [podcast_id])
        podcast_details = cursor.fetchone()
        if podcast_details:
            total_durasi = podcast_details[4]
            hours = total_durasi // 60
            minutes = total_durasi % 60
            formatted_duration = f"{hours} jam {minutes} menit" if hours > 0 else f"{minutes} menit"
            data_podcast = {
                'judul': podcast_details[0],
                'tanggal_rilis': podcast_details[1],
                'tahun': podcast_details[2],
                'podcaster': podcast_details[3],
                'total_durasi': formatted_duration
            }

    # Query to get genres
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT genre FROM marmut.genre WHERE id_konten = %s
        """, [podcast_id])
        genres = cursor.fetchall()
    if genres:
        data_podcast['genre'] = [row[0] for row in genres]

    # Query to get episodes details
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT judul, deskripsi, durasi, tanggal_rilis
            FROM marmut.episode
            WHERE id_konten_podcast = %s
        """, [podcast_id])
        episodes = cursor.fetchall()
    for episode in episodes:
        duration_hours = episode[2] // 60
        duration_minutes = episode[2] % 60
        formatted_duration = f"{duration_hours} jam {duration_minutes} menit" if duration_hours else f"{duration_minutes} menit"

        data_episode.append({
            'title': episode[0],
            'description': episode[1],
            'duration': formatted_duration,
            'date': episode[3].strftime('%d/%m/%Y')
        })

    context = {
        'detail_podcast': data_podcast,
        'kumpulan_episode': data_episode
    }

    return render(request, 'playpodcast.html', context)

def delete_podcast(request):
    podcast_id = request.POST.get('podcast_id')
    
    with connection.cursor() as cursor:
        cursor.execute(
            'DELETE FROM marmut.podcast WHERE id_konten = %s', [podcast_id]
        )
        cursor.execute(
            'DELETE FROM marmut.konten WHERE id = %s', [podcast_id]
        )
        connection.commit()
    
    return HttpResponseRedirect(reverse('podcast:list_podcast'))

@csrf_exempt
def delete_episode(request):
    episode_id = request.POST.get('episode_id')
    podcast_id = request.POST.get('podcast_id')
    
    print("podcast id :")
    print(podcast_id)
    with connection.cursor() as cursor:
        cursor.execute(
            'DELETE FROM marmut.episode WHERE id_episode = %s', [episode_id]
        )
        connection.commit()
    
    return HttpResponseRedirect(reverse('podcast:daftar_episode') + f'?podcast={podcast_id}')