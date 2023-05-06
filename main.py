import pandas as pd

from scraper import scrape_people_also_ask
from media_fetcher import fetch_images, fetch_videos
from optimizer import optimize_content
from data_processor import merge_data, store_data


def main():
    # Read in the keywords from a CSV file
    df = pd.read_csv("keywords.csv")

    # Initialize an empty list to store the data
    data = []

    # Loop through the keywords and scrape the PAA sections
    for index, row in df.iterrows():
        paa_data = scrape_people_also_ask(row['keyword'])

        # Fetch images and videos related to the keyword
        media_data = {
            'images': fetch_images(row['keyword']),
            'videos': fetch_videos(row['keyword'])
        }

        # Merge the PAA data and media data into a single dictionary
        content_data = merge_data(paa_data, media_data)

        # Optimize the content using AI tools
        optimized_data = optimize_content(content_data)

        # Append the optimized data to the list
        data.append(optimized_data)

    # Store and process the data
    store_data(data)

if __name__ == "__main__":
    main()
