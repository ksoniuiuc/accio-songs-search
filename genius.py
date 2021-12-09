import lyricsgenius as lg

class GENIUS:

    def __init__(self, config) -> None:
        self.genius = lg.Genius(access_token=config["genius_api"]["access_token"])

        print(self.genius)


    def get_lyrics(self, artist_name, track_title):
        try:
            track = self.genius.search_song(title=track_title, artist=artist_name)
            track_lyrics = track.lyrics

        except:
            track_lyrics = "NO LYRICS AVAILABLE"

        return track_lyrics