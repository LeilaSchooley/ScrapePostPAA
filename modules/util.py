import os
import random
import string
import time

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from twocaptcha import TwoCaptcha
import requests
from PIL import Image

def randomword(length):
    import random

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
def download_file_requests(link):
    s = requests.Session()

    r = s.get(link, timeout=30)

    f = open(f"{randomword}.jpeg", 'wb')
    print("Downloading.....")
    for chunk in r.iter_content(chunk_size=255):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

def resize_to_featured_post_size(path):
    image = Image.open('/example/path/to/image/file.jpg/')
    image.thumbnail((80, 80), Image.ANTIALIAS)
    image.save('/some/path/thumb.jpg', 'JPEG', quality=88)

def check_if_file_exists(path):
    return os.path.isfile(path)


def human_type(element, text):
    for char in text:
        time.sleep(random.uniform(0.1,0.5))  # fixed a . instead of a
        element.type(char)

def solve_recaptcha(current_url, captcha_key, sitekey):
    solver = TwoCaptcha(captcha_key)

    result = solver.recaptcha(sitekey=sitekey,
                              url=current_url)

    return result["code"]


def merge_data(paa_data, media_data):
    # Create a new dictionary to store the merged data
    merged_data = {}

    # Loop through the PAA data and add it to the merged dictionary
    for question, answer in paa_data.items():
        merged_data[question] = {"answer": answer}

    # Loop through the media data and add it to the merged dictionary
    for media_type, media_url in media_data.items():
        if media_type == "image":
            merged_data["image_url"] = media_url
        elif media_type == "video":
            merged_data["video_url"] = media_url

    return merged_data
