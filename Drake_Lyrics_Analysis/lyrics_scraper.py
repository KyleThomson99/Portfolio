import requests
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

from lyric_search import *

base = "https://api.genius.com"
client_access_token  = "ys-Hvja24uT_FUN5GOBotqi1A52kGCDodUz1bo63C-zcTxXASgba_7ESi2BAJolt"

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
        