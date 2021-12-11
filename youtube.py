import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YOUTUBE:
    def __init__(self, config) -> None:
        self.DEVELOPER_KEY = config["youtube_api"]["developer_key"]
        self.YOUTUBE_API_SERVICE_NAME = config["youtube_api"]["service_name"]
        self.YOUTUBE_API_VERSION = config["youtube_api"]["version"]


    def youtube_search(self, query):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)
        # Call the search.list method to retrieve results matching the specified
        # query term.
        try:
            #print(query)
            search_response = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            order='relevance',
            maxResults=1
            ).execute()

            videos = []
            # channels = []
            # playlists = []

            # Add each result to the appropriate list, and then display the lists of
            # matching videos, channels, and playlists.
            search_result = search_response.get('items')[0]
            # if search_result['id']['kind'] == 'youtube#video':
            video_title = search_result['snippet']
            video_id = search_result['id']['videoId']
            video_url = f'https://www.youtube.com/embed/{search_result["id"]["videoId"]}?autoplay=0'
            videos.append(f'{video_title} \n({video_id}) \n{video_url}\n\n')

            # elif search_result['id']['kind'] == 'youtube#channel':
            #     channels.append('%s (%s)' % (search_result['snippet']['title'],
            #                                 search_result['id']['channelId']))
            # elif search_result['id']['kind'] == 'youtube#playlist':
            #     playlists.append('%s (%s)' % (search_result['snippet']['title'],
            #                                 search_result['id']['playlistId']))

            # print(f'Videos: {" ".join(videos)}')
            
            # print(f'Channels: {" ".join(channels)}')
            # print(f'Playlists: {" ".join(playlists)}')

            return video_url

        except HttpError as e:
                print(f'An HTTP error {e.resp.status} occurred:\n {e.content}')
                return ""
                
