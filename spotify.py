import os
import json

import spotipy

from spotipy.oauth2 import SpotifyOAuth

class SPOTIFY:

    def __init__(self, config):
        authObject = spotipy.SpotifyOAuth(client_id=config["spotify_api_auth"]["client_id"],
                                        client_secret=config["spotify_api_auth"]["client_secret"],
                                        redirect_uri=config["spotify_api_auth"]["redirect_uri"],
                                        scope=config["spotify_api_auth"]["scope"])

        print(authObject)

        token_dict = authObject.get_access_token()

        print(token_dict)

        self.access_token = token_dict["access_token"]

        self.spotify_object = spotipy.Spotify(auth=self.access_token)

        print(self.spotify_object)


        # results = sp.current_user_saved_tracks()
        # for idx, item in enumerate(results['items']):
        #     track = item['track']
        #     print(idx, track['artists'][0]['name'], " – ", track['name'])


        # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config["spotify_api_auth"]["client_id"],
        #                                                            client_secret=config["spotify_api_auth"]["client_secret"]))

    def get_data(self, query, search_type):
        result = {}
        
        data = self.spotify_object.search(q=query, type=search_type.rstrip('s'), limit=10)
        
        if 'artists' == search_type:
            with open('data/artists_all.json', 'w') as data_file:
                json.dump(data, data_file)
            print(f'Search Type = {search_type}')
        
            all_artist_data = []
            
            for artist in data['artists']['items']:
                artist_data = {}
                artist_data['id'] = artist['id']
                artist_data['name'] = artist['name']
                artist_data['followers'] = artist['followers']['total']
                artist_data['popularity'] = artist['popularity']
                artist_data['genres'] = artist['genres']
                artist_data['image'] = artist['images'] #[0]['url'] if artist['images'] else ""
                if artist_data['followers'] > 0 and artist_data['popularity'] > 0:
                    all_artist_data.append(artist_data)
            
            if all_artist_data:
                with open('data/artists.json', 'w') as data_file:
                    json.dump(all_artist_data, data_file)
                result = all_artist_data


        elif 'albums' == search_type:
            album_data = data['albums']['items']
            with open('data/albums_all.json', 'w') as data_file:
                json.dump(data, data_file)
            print(f'Search Type = {search_type}')

            all_album_data = []
            
            for album in data['albums']['items']:
                album_data = {}
                album_data['id'] = album['id']
                album_data['name'] = album['name']
                album_data['artists'] = album['artists']
                album_data['release_date'] = album['release_date']
                album_data['total_tracks'] = album['total_tracks']
                album_data['image'] = album['images'][0]['url'] if album['images'] else ""
                if album_data['total_tracks'] > 0:
                    all_album_data.append(album_data)
            
            if all_album_data:
                with open('data/albums.json', 'w') as data_file:
                    json.dump(all_album_data, data_file)
                result = all_album_data
        
        elif 'tracks' == search_type:
            track_data = data['tracks']['items']
            if track_data:
                with open('data/tracks.json', 'w') as data_file:
                    json.dump(data, data_file)
                result = track_data

        return result

