import os
import json
from elastic_enterprise_search import AppSearch
from flask import Flask, session, render_template, request
from flask_session import Session
import time
import uuid
import spotipy

# Spotify Class Import
from spotify import SPOTIFY


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    cache_file = caches_folder + session.get('uuid')

    token_data = {"access_token": "BQAM1rq_CplfdOkZQjAuEclqCpRfYq-Q85fJpVHG1aKu1a_wThATibDjGZqLd5jqARtP4sM5K6aV6LmxcVGAyHy4-8TF6OmgM2nXqKZuMmxxyrKwg_1RZj8NaXnnLdqQBEHtTbcwNScEcDTGeuSPRvY2xTCjGw", "token_type": "Bearer",
                  "expires_in": 3600, "refresh_token": "AQCMrVYFkXdpmpHwvYlmYogE0pN-oRd4bM9YqnjxyRELPqkZyLJFw4OF6sOOHvp4rwQWN2uko34Vfi0q6U38NH-2IxUn19SAM9SuFYNPoWuSWgddLFplQ4EvIiHczBSyQV0", "scope": "user-library-read", "expires_at": 1639133912}
    with open(cache_file, 'w+') as data_file:
        json.dump(token_data, data_file)
    return cache_file


with open("config.json") as config_file:
    config = json.load(config_file)

client = AppSearch(
    config['appsearch']['base_endpoint'],
    http_auth=config['appsearch']['api_key'])

engine_name = config['appsearch']['engine_name']


# Home page Route definition
@app.route("/", methods=['GET'])
def home():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())

    # Spotify API Details
    spotify_obj = SPOTIFY(config, cache_handler)

    session['spotify_obj'] = spotify_obj

    # Initializing default Search Type to "artist"
    return render_template("layout.html", search_type="")


@app.route("/artists/<query>", methods=['GET', 'POST'])
def artists(query):
    print(f'query {query}')
    print(f'request.form {request.form}')
    search_type = request.form['search_type']
    print(f'search_type {search_type}')
    if query != "":
        data = client.search(engine_name, body={
            "query": query,
            "sort": [
                {"followers": "desc"},
                {"popularity": "desc"},
                {"name": "desc"}
            ],
            "filters": {
                "type": "artist"
            }
        })
        api_response = ""
        if not data["results"] or len(data["results"]) < 20:
            api_response = get_api_data(query, search_type)
            data = client.search(engine_name, body={
                "query": query,
                "sort": [
                    {"followers": "desc"},
                    {"popularity": "desc"},
                    {"name": "desc"}
                ],
                "filters": {
                    "type": "artist"
                }
            })

        if len(data["results"]) > 0 or api_response != "": 
            api_response = "Artists Summoned !!!"
            # with open('data/data.json', 'w+') as outfile:
            #     json.dump(data, outfile)
        #print(data['results'])
    else:
        data = None
        api_response = 'Please Enter text in the Search Bar...'
    return render_template("artists.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Artists')


@app.route("/albums/<query>", methods=['GET', 'POST'])
def albums(query):
    search_type = request.form['search_type']
    print(f'query {query}')
    
    if query != "":
        data = client.search(engine_name, body={
            "query": query,
            "sort": [
                {"release_date": "desc"},
                {"total_tracks": "desc"},
                {"name": "asc"}
            ],
            "filters": {
                "type": "album"
            }
        })
        api_response = ""
        if not data["results"] or len(data["results"]) < 10:
            api_response = get_api_data(query, search_type)
            data = client.search(engine_name, body={
                "query": query,
                "sort": [
                    {"release_date": "desc"},
                    {"total_tracks": "desc"},
                    {"name": "asc"}
                ],
                "filters": {
                    "type": "album"
                }
            })

        print(len(data["results"]), api_response)
        if len(data["results"]) > 0 or api_response != "": 
            api_response = "Albums Summoned !!!"
            # with open('data/data.json', 'w+') as outfile:
            #     json.dump(data, outfile)
        #print(data['results'])
    else:
        data = None
        api_response = 'Please Enter text in the Search Bar...'
    return render_template("albums.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Albums')


@app.route("/artist_albums/id/<artist_id>", methods=['GET', 'POST'])
def artist_albums(artist_id):
    print(f'artist_id {artist_id}')
    search_type = 'artist-albums'
    data = client.search(engine_name, body={
        "query": artist_id,
        "search_fields": {
            "artists": {}
        },
        "sort": [
            {"release_date": "desc"},
            {"total_tracks": "desc"},
            {"name": "asc"}
        ],
        "filters": {
            "type": "album"
        }
    })
    api_response = ""
    if not data["results"] or len(data["results"]) < 10:
        api_response = get_api_data(artist_id, search_type)
        data = client.search(engine_name, body={
            "query": artist_id,
            "search_fields": {
                "artists": {}
            },
            "sort": [
                {"release_date": "desc"},
                {"total_tracks": "desc"},
                {"name": "asc"}
            ],
            "filters": {
                "type": "album"
            }
        })
    
    if len(data["results"]) > 0 or api_response != "": 
        api_response = "Albums Summoned !!!"
        # with open('data/data.json', 'w+') as outfile:
        #     json.dump(data, outfile)
    #print(data['results'])
    search_type = 'albums'
    return render_template("albums.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Artist - Albums')


@app.route("/tracks/<query>", methods=['GET', 'POST'])
def tracks(query):
    search_type = request.form['search_type']
    print(f'query {query}')
    if query != "":
        data = client.search(engine_name, body={
            "query": query,
            "search_fields": {
                "name": {}
            },
            "sort": [
                {"popularity": "desc"},
                {"duration": "desc"},
                {"name": "asc"}
            ],
            "filters": {
                "type": "track"
            }
        })

        api_response = ""
        if not data["results"] or len(data["results"]) < 10:
            api_response = get_api_data(query, search_type)
            data = client.search(engine_name, body={
                "query": query,
                "search_fields": {
                    "name": {}
                },
                "sort": [
                    {"popularity": "desc"},
                    {"duration": "desc"},
                    {"name": "asc"}
                ],
                "filters": {
                    "type": "track"
                }
            })
        
        if len(data["results"]) > 0 or api_response != "": 
            api_response = "Tracks Summoned !!!"
            # with open('data/data.json', 'w+') as outfile:
            #     json.dump(data, outfile)
        #print(data['results'])
    else:
        data = None
        api_response = 'Please Enter text in the Search Bar...'
    return render_template("tracks.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Tracks')


@app.route("/album_tracks/id/<album_id>", methods=['GET', 'POST'])
def album_tracks(album_id):
    search_type = 'album-tracks'
    print(f'album_id {album_id}')
    data = client.search(engine_name, body={
        "query": "",
        "sort": [
            {"album": "asc"},
            {"popularity": "desc"},
            {"name": "asc"}
        ],
        "filters": {
            "all": [
                {"type": "track"},
                {"album_id": album_id}
            ]
        }
    })
    api_response = ""
    if not data["results"] or len(data["results"]) < 10:
        print("Track HERE")
        print(album_id)
        api_response = get_api_data(album_id, search_type)
        data = client.search(engine_name, body={
            "query": "",
            "sort": [
                {"album": "asc"},
                {"popularity": "desc"},
                {"name": "asc"}
            ],
            "filters": {
                "all": [
                    {"type": "track"},
                    {"album_id": album_id}
                ],
            }
        })
    
    if len(data["results"]) > 0 or api_response != "": 
        api_response = "Tracks Summoned !!!"
        # with open('data/data.json', 'w+') as outfile:
        #     json.dump(data, outfile)

    search_type = 'tracks'
    return render_template("tracks.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Album - Tracks')


@app.route("/track_details/id/<track_id>", methods=['GET', 'POST'])
def track_details(track_id):
    search_type = 'track-details'
    print(f'track_id {track_id}')

    data = client.search(engine_name, body={
        "query": track_id,
        "search_fields": {
            "id": {}
        },
        "sort": [
            {"popularity": "desc"},
            {"duration": "desc"},
            {"name": "asc"}
        ],
        "filters": {
            "type": "track"
        }
    })
    
    print(data["results"])
    api_response = ""
    if len(data["results"]) == 0 or ('lyrics' not in data["results"][0] or 'youtube_url' not in data["results"][0]):
        api_response = get_api_data(track_id, search_type)
        data = client.search(engine_name, body={
            "query": "",
            "search_fields": {
                "name": {}
            },
            "sort": [
                {"popularity": "desc"},
                {"duration": "desc"},
                {"name": "asc"}
            ],
            "filters": {
                "all": [
                    {"type": "track"},
                    {"spotify_id": track_id}
                ],
            }
        })
    
    if len(data["results"]) > 0 or api_response != "": 
        api_response = "Details Summoned !!!"
        # with open('data/data.json', 'w+') as outfile:
        #     json.dump(data, outfile)

    search_type = 'tracks'
    return render_template("track_details.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Track Details')


def get_api_data(query, search_type):
    spotify_obj = session['spotify_obj']
    api_data = spotify_obj.get_data(query, search_type, session)
    response = []
    if api_data:
        response = client.index_documents(engine_name, api_data)
        time.sleep(1.0)
        # print(f'response {response}')
        return response

    return []


@app.route("/delete")
def delete():
    # get data from the client
    data = client.list_documents(engine_name)
    #data = client.index_documents(engine_name, documents)
    doc_ids = [items['id'] for items in data['results']]
    if doc_ids:
        data = client.delete_documents(engine_name, document_ids=doc_ids)
    return render_template("layout.html", data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=False)
