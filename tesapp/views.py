from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_akun(request):
    query_str = "SELECT * FROM akun"
    hasil = query(query_str)
    return render(request, 'index.html', {'akun': hasil})

# Create your views here.
def show_konten(request):
    query_str = "SELECT * FROM konten"
    hasil = query(query_str)
    return render(request, 'konten.html', {'konten': hasil})


#ngetes doang