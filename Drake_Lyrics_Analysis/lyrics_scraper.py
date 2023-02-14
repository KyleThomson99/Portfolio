import requests
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

from search_functions import *

base = "https://api.genius.com"
client_access_token  = "TczpRGqWv-BdhRtJQ0WeQg5HQxGSANb_LzKl5qYgLynMcnNzTgAfsO6FSUxqXdta"

def get_lyrics_path(song_id):
    song_url = f"songs/{song_id}"
    data = get_json(song_url)
    path = data['response']['song']['path']

    return path

def get_songs_id(artist_id):
    current_page = 1
    next_page = True
    songs = []

    while next_page:
        path = "artists/{}/songs".format(artist_id)
        params = {'page': current_page}
        data = get_json(path = path, params = params)

    page_songs = data['response']['songs']
    if page_songs:
        songs += page_songs
        current_page += 1
        print('Page {} finished scraping'.format(current_page))
    else:
        next_page = False

    print('Song id were scraped from {} pages'.format(current_page))

    songs = [song['id'] for song in songs if song['primary_artist']['id'] == artist_id]

    return songs

print(get_songs_id(72))