import json
from elastic_enterprise_search import AppSearch
from flask import Flask, render_template, request
import requests
import time

# Spotify Class Import
from spotify import SPOTIFY

# Genius Class Import
from genius import GENIUS

app = Flask(__name__)


with open("config.json") as config_file:
    config = json.load(config_file)

client = AppSearch(
    config['appsearch']['base_endpoint'],
    http_auth=config['appsearch']['api_key'])

engine_name = config['appsearch']['engine_name']


# Spotify API Details
spotify_obj = SPOTIFY(config)


# Spotify API Details
genius_obj = GENIUS(config)


# Musix Match
api_url = config['musix_match_api']['url']
api_key = config['musix_match_api']['key']
api_format = config['musix_match_api']['format']


app.run(debug=False)