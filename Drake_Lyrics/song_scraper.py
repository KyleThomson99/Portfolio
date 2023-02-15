import requests
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
import pandas as pd

base = "https://api.genius.com"
client_access_token  = "TczpRGqWv-BdhRtJQ0WeQg5HQxGSANb_LzKl5qYgLynMcnNzTgAfsO6FSUxqXdta"

def get_json(path, params = None, header = None):
    requrl = '/'.join([base,path])
    token = 'Bearer {}'.format(client_access_token)
    if header:
        header['Authorization'] = token
    else:
        header = {'Authorization': token}
    
    response = requests.get(url = requrl, params = params, headers = header)
    response.raise_for_status()

    return response.json()

def get_song_ids(artist_id):
    current_page = 1
    next_page = True
    songs = []

    while next_page:
        path = "artists/{}/songs/".format(artist_id)
        params = {'page': current_page}
        data = get_json(path = path, params = params)

        page_songs = data['response']['songs']
        if page_songs:
            songs += page_songs
            current_page += 1
            print('Page {} finished scraping'.format(current_page))
        
        else:
            next_page = False


    print('Song ids were scraped from {} pages'.format(current_page))

    song_ids = [song['id'] for song in songs if song['primary_artist']['id'] == artist_id]

    return song_ids

def get_song_info(song_ids):
    song_list = {}
    for i, song_id in enumerate(song_ids):
        print("id: " + str(song_id) + " start. ->")

        path = "songs/{}".format(song_id)
        data = get_json(path = path)['response']['song']

        song_list.update({
            i : {
                'title' : data['title'],
                'album' : data['album']['name'] if data['album'] else '<single>',
                'release_date' : data['release_date'] if data['release_date'] else None,
                'featured_artists' : 
                    [feat['name'] if data['featured_artists'] else None for feat in data['featured_artists']],
                'producer_artists' : 
                    [feat['name'] if data['producer_artists'] else None for feat in data['producer_artists']],
                'writer_artists':
                    [feat['name'] if data['writer_artists'] else None for feat in data['writer_artists']],
                'genius_track_id' : song_id,
                'genius_album_id' : data['album']['id'] if data['album'] else None
            }
        })

        print("-> id:" + str(song_id) + 'is finished. \n')
    
    return song_list

def main():
    search_term = 'Drake'
    artist_id = 130
    
    song_ids = get_song_ids(130)

    song_list = get_song_info(song_ids)
    df = pd.DataFrame.from_dict(song_list, orient = 'index')
    df.to_csv('drake_songs.csv')



if __name__ == "__main__":
    main()