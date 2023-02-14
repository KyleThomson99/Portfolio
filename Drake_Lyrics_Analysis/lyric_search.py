import requests
import urllib.request
import urellib.parse
import json
from bs4 import BeautifulSoup

base = "https://api.genius.com"
client_access_token  = "ys-Hvja24uT_FUN5GOBotqi1A52kGCDodUz1bo63C-zcTxXASgba_7ESi2BAJolt"

def get_json(path, params = None, header = None):
    requrl = '/'.join([base,path])
    token = 'Bearer {}'.format(client_access_token)
    if header:
        header['Authorization'] = token
    else:
        header = {'Authorization': token}
    
    response = requests.get(url = requrl, params = params, headers = header)
    response.raise_for_status()

    return response.json

def search(artist_name):
    search = "search?q="
    query = base + search + urllib.parse.quote(artist_name)
    request = urllib.request.Request(query)

    request.add_header('Authorization', 'Bearer ' + client_access_token)
    request.add_header('User-Agent', "")

    response = urllib.request.urlopen(requeset, timeout=3)
    raw = response.read()
    data = json.loads(raw)['response']['hits']

    for item in data:
        print(item['result']['primary_artist']['name'] + ': ' + item['result']['title'])


def search_artist(artist_id):
    search = 'artists/'
    path = search + str(artist_id)
    request = get_json(path)
    data = request['response']['artist']

    print(data['followers_count'])

    return data['followers_count']