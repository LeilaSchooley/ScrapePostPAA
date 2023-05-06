import configparser
import os

import requests
from pyunsplash import PyUnsplash

from modules.util import download_file_requests

# Read the config file
config_path = os.path.join(os.path.dirname(__file__), '../data/', 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

# Access the API keys
YOUTUBE_API_KEY = config["DEFAULT"]["YOUTUBE_API_KEY"]
UNSPLASH_API_KEY = config["DEFAULT"]["UNSPLASH_API_KEY"]

class RelatedMediaFetcher:
    def __init__(self):
        pass


    def fetch_related_videos(self, query):
        # code to fetch related videos

        # Set the API key and the query parameters

        max_results = 25

        # Make the API request
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "key": YOUTUBE_API_KEY,
                "part": "snippet",
                "q": query,
                "maxResults": max_results,
                "type": "video",
            },
        )

        # Get the list of videos from the response
        videos = response.json()["items"]

        # Print the video titles
        for video in videos:
            print(video["snippet"]["title"])
            print(video["id"]["videoId"])


    def fetch_related_images(self, query):
        # code to fetch related images
        pu = PyUnsplash(api_key=UNSPLASH_API_KEY)

        photos = pu.photos(type_='random', count=10, featured=True, query=query)
        for photo in photos.entries:
            print(photo.id, photo.link_download)


        # download_file_requests(  "https://unsplash.com/photos/K2Y6sBLGd48/download?ixid=MnwxNDc0MDF8MHwxfHJhbmRvbXx8fHx8fHx8fDE2NjgwMzcwNzI")


related_media_fetcher = RelatedMediaFetcher()

# fetch related videos
related_media_fetcher.fetch_related_videos()

# fetch related images
related_media_fetcher.fetch_related_images()
