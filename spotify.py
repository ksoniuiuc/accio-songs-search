import base64
import os
import json
from lyricsgenius import genius
import requests
import six

import spotipy

from spotipy.oauth2 import SpotifyOAuth


# Genius Class Import
from genius import GENIUS

# Genius Class Import
from youtube import YOUTUBE

# def _make_authorization_headers(client_id, client_secret):
#     auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
#     return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

class SPOTIFY:

    def __init__(self, config, cache_handler):
        self.authObject = SpotifyOAuth(client_id=config["spotify_api_auth"]["client_id"],
                                        client_secret=config["spotify_api_auth"]["client_secret"],
                                        redirect_uri=config["spotify_api_auth"]["redirect_uri"],
                                        scope=config["spotify_api_auth"]["scope"],
                                        cache_handler=cache_handler)
        
        print(cache_handler)
        self.token_info = self.authObject.get_access_token()

        self.access_token = self.token_info["access_token"]

        self.spotify_object = spotipy.Spotify(auth=self.access_token)

    
        print(self.spotify_object)

        # Genius API Details
        self.genius_obj = GENIUS(config)

        print(self.genius_obj)

        # YouTube API Details
        self.youtube_obj = YOUTUBE(config)

        print(self.youtube_obj)

    def refresh(self):
        if self.authObject.is_token_expired(self.token_info):
            self.token_info = self.authObject.refresh_access_token(self.token_info['refresh_token'])
            token = self.token_info['access_token']
            self.spotify_object = spotipy.Spotify(auth=token)



    def get_data(self, query, search_type, session):
        print(f'Is token Expired ? {self.authObject.is_token_expired(self.token_info)}')
        if self.authObject.is_token_expired(self.token_info):
            print("TOKEN EXPIRED !!!!")
            self.refresh()
        
        #print(query, search_type, session)
        result = {}
        spotify_data = {}
        if search_type == 'artist-albums':
            spotify_data = self.spotify_object.artist_albums(artist_id=query, limit=20)

        elif search_type == 'album-tracks':
            spotify_data = self.spotify_object.album_tracks(album_id=query)
            # with open('data/tracks_all.json', 'w+') as data_file:
            #     json.dump(spotify_data, data_file)

        elif search_type == 'track-details':
            track_id = query
            #spotify_data = self.spotify_object.track(q=track_id, type='track', limit=1)

        else:            
            spotify_data = self.spotify_object.search(q=query, type=search_type.rstrip('s'), limit=20)
        
        if 'artists' == search_type:            
            artists_api_data = spotify_data['artists']['items']
            # with open('data/artists_all.json', 'w+') as data_file:
            #     json.dump(spotify_data, data_file)
            # print(f'Search Type = {search_type}')
        
            all_artist_data = []
            
            for artist in artists_api_data:
                artist_data = {}
                artist_data['type'] = 'artist'
                artist_data['spotify_id'] = artist['id']
                artist_data['id'] = artist['id']
                artist_data['name'] = artist['name']
                artist_data['followers'] = artist['followers']['total']
                artist_data['popularity'] = artist['popularity']
                artist_data['genres'] = artist['genres']
                artist_data['image'] = artist['images'] #[0]['url'] if artist['images'] else ""
                if artist_data['followers'] > 0 and artist_data['popularity'] > 0:
                    all_artist_data.append(artist_data)
            
            if all_artist_data:
                # with open('data/artists.json', 'w+') as data_file:
                #     json.dump(all_artist_data, data_file)
                result = all_artist_data


        elif search_type in ('albums', 'artist-albums'):
            if 'albums' in spotify_data.keys():
                album_api_data = spotify_data['albums']['items']
            else:
                album_api_data = spotify_data['items']
            # with open('data/albums_all.json', 'w+') as data_file:
            #     json.dump(spotify_data, data_file)
            print(f'Search Type = {search_type}')

            all_album_data = []
            duplicate_check = {}
            for album in album_api_data:
                album_data = {}
                album_data['type'] = 'album'
                album_data['spotify_id'] = album['id']
                album_data['id'] = album['id']
                album_data['name'] = album['name']
                album_data['artists'] = album['artists']
                album_data['release_date'] = album['release_date']
                album_data['total_tracks'] = album['total_tracks']
                album_data['image'] = album['images'] #[0]['url'] if album['images'] else ""
                
                if album_data['total_tracks'] > 0:
                    if album_data['name'].lower() not in duplicate_check or \
                    duplicate_check[album_data['name'].lower()] != album_data['artists']:
                        duplicate_check[album_data['name'].lower()] = album_data['artists']
                        all_album_data.append(album_data)
            
            if all_album_data:
                # with open('data/albums.json', 'w+') as data_file:
                #     json.dump(all_album_data, data_file)
                result = all_album_data
        
        elif search_type in ('tracks', 'album-tracks'):
            if 'tracks' in spotify_data.keys():
                album_data = []
                track_api_data = spotify_data['tracks']['items']
            else:
                album_data = self.spotify_object.album(album_id=query)
                track_api_data = album_data['tracks']['items']
            
            with open('tracks_all.json', 'w+') as data_file:
                json.dump(spotify_data, data_file)
            print(f'Search Type = {search_type}')

            all_track_data = []
            
            duplicate_check = {}
            for track in track_api_data:
                track_data = {}
                track_data['type'] = 'track'
                track_data['spotify_id'] = track['id']
                track_data['id'] = track['id']
                track_data['name'] = track['name']
                # if search_type == 'album-tracks':
                #     spotify_data = self.spotify_object.album(album_id=query)
                #     track_data['album'] = spotify_data
                #     track_data['popularity'] = spotify_data['popularity']
                #     track_data['image'] = spotify_data['images'][0]['url'] if spotify_data['images'][0]['url'] else ""
                # else:
                #     track_data['album'] = track['album']
                #     track_data['popularity'] = track['popularity']
                #     track_data['image'] = track['album']['images'][0]['url'] if track['album']['images'][0]['url'] else ""

                if album_data:
                    track_data['album'] = album_data['name']
                    track_data['album_id'] = album_data['id']
                    track_data['popularity'] = album_data['popularity']
                    track_data['image'] = album_data['images'][0]['url'] if album_data['images'][0]['url'] else ""
                else:                    
                    track_data['album'] = track['album']['name']
                    track_data['album_id'] = track['album']['id']
                    track_data['popularity'] = track['popularity']
                    track_data['image'] = track['album']['images'][0]['url'] if track['album']['images'][0]['url'] else ""

                track_data['artists'] = track['artists']
                track_data['duration'] = round(float(track['duration_ms'])/60000, 2)
                track_data['explicit'] = track['explicit']
                track_data['spotify_url'] = track['external_urls']['spotify'].replace('/track', '/embed/track')
                track_data['preview_url'] = track['preview_url']

                
                

                if track_data['duration'] > 0:
                    if track_data['name'].lower() not in duplicate_check or \
                    duplicate_check[track_data['name'].lower()] != track_data['album'].lower() + str(len(track_data['artists'])):
                        duplicate_check[track_data['name'].lower()] = track_data['album'].lower() + str(len(track_data['artists']))
                
                        all_track_data.append(track_data)
                    
            
            if all_track_data:
                session['track_data'] = all_track_data
                # with open('tracks.json', 'w+') as data_file:
                #     json.dump(all_track_data, data_file)
                result = all_track_data

        elif search_type in ('track-details'):
            # with open('data/tracks.json') as f:
            #     track_json_data = json.load(f)
            track_json_data = session['track_data']
            track = {}
            for item in track_json_data:
                if item['id'] == query:
                    track = item
            
            track_data = {}
            track_data['type'] = 'track'
            track_data['spotify_id'] = track['id']
            track_data['id'] = track['id']
            track_data['name'] = track['name']
            track_data['album'] = track['album']
            track_data['album_id'] = track['album_id']
            track_data['popularity'] = track['popularity']
            track_data['image'] = track['image']

            track_data['artists'] = track['artists']
            track_data['duration'] = track['duration']
            track_data['explicit'] = track['explicit']
            track_data['spotify_url'] = track['spotify_url']
            track_data['preview_url'] = track['preview_url']
            track_name_genius = " ".join((track_data['name'].split('('))[:1])
            track_artist_genius = track['artists'][0]['name']
            track_data['lyrics'] = self.genius_obj.get_lyrics(track_name_genius, track_artist_genius)

            ## Get YouTube URL
            youtube_query = f"{track_name_genius} {track_artist_genius}"
            track_data['youtube_url'] = self.youtube_obj.youtube_search(youtube_query)
            
            # with open('data/lyrics.json', 'w+') as data_file:
            #         json.dump(track_data, data_file)
            result = track_data

        return result
