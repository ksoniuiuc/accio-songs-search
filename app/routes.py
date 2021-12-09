from app import *


# Home page Route definition
@app.route("/", methods=['GET'])
def home():
    data = client.search(engine_name, body={
        "query": ""
    })

    # Initializing default Search Type to "artist"
    return render_template("layout.html", data=data['results'], search_type="")


@app.route("/artists/<query>", methods=['GET', 'POST'])
def artists(query):
    print("Here")
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
            api_response = "Data Found" if api_response else ""
            with open('data/data.json', 'w+') as outfile:
                json.dump(data, outfile)
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
        if not data["results"] or len(data["results"]) < 20:
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
            api_response = "Data Found" if api_response else ""
            with open('data/data.json', 'w+') as outfile:
                json.dump(data, outfile)
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
    if not data["results"] or len(data["results"]) <= 10:
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
        api_response = "Data Found" if api_response else ""
        with open('data/data.json', 'w+') as outfile:
            json.dump(data, outfile)
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
        if not data["results"] or len(data["results"]) < 20:
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
            api_response = "Data Found" if api_response else ""
            with open('data/data.json', 'w+') as outfile:
                json.dump(data, outfile)
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
    if not data["results"] or len(data["results"]) <= 10:
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
        api_response = "Data Found" if api_response else ""
        with open('data/data.json', 'w+') as outfile:
            json.dump(data, outfile)

    search_type = 'tracks'
    return render_template("tracks.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Album - Tracks')



@app.route("/lyrics/<query>", methods=['GET', 'POST'])
def lyrics(query):
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
        if not data["results"] or len(data["results"]) < 20:
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
            api_response = "Data Found" if api_response else ""
            with open('data/data.json', 'w+') as outfile:
                json.dump(data, outfile)
        #print(data['results'])
    else:
        data = None
        api_response = 'Please Enter text in the Search Bar...'
    return render_template("lyrics.html", data=data,
                           api_response=api_response if api_response else "No Data Found",
                           search_type=search_type, title='Lyrics')



def get_api_data(query, search_type):
    api_data = spotify_obj.get_data(query, search_type)
    response = []
    if api_data:
        response = client.index_documents(engine_name, api_data)
        time.sleep(1.0)
        print(f'response {response}')
        return response

    return []


@app.route("/index")
def index():
    # Opening JSON file
    f = open('data/data.json', )

    # returns JSON object as
    # a dictionary
    documents = json.load(f)
    data = client.list_documents(engine_name)
    #data = client.index_documents(engine_name, documents)
    data = [items['id'] for items in data['results']]
    return render_template("about.html", data=data)


@app.route("/delete")
def delete():
    # get data from the client
    data = client.list_documents(engine_name)
    #data = client.index_documents(engine_name, documents)
    doc_ids = [items['id'] for items in data['results']]
    if doc_ids:
        data = client.delete_documents(engine_name, document_ids=doc_ids)
    return render_template("layout.html", data=data)


def read(query, search_type):
    matcher = "track.search"
    if search_type == 'artist':
        matcher_string = f'&q_artist={query}'
        rating_criteria = f'&s_{search_type}_rating'

    elif search_type == 'track':
        matcher_string = f'&q_track={query}'
        rating_criteria = f'&s_{search_type}_rating'
    else:
        matcher_string = f'&q_lyrics={query}'
        rating_criteria = f'&s_track_rating'

    api_call = api_url + matcher + api_format + \
        matcher_string + rating_criteria + api_key
    request = requests.get(api_call)
    data = request.json()
    data = [item['track'] for item in data['message']["body"]['track_list']]
    #print(data)
    if data:
        with open('data/data.json', 'w+') as outfile:
            json.dump(data, outfile)
        response = client.index_documents(engine_name, data)
        time.sleep(0.1)
        return response
    else:
        return []
