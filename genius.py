import os
import json
import lyricsgenius as lg


with open("config.json") as config_file:
    config = json.load(config_file)

genius_object = lg.Genius(access_token=config["genius_api"]["access_token"])

print(genius_object)