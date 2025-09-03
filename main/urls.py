# ini adalah file yang berisi konfigurasi routing untuk aplikasi main
from django.urls import path
from main.views import show_main

app_name = "main"

urlpatterns = [
    # fungsi path() dari modul django.urls mendefinisikan pola URL
    path('', show_main, name="show_main"),
]